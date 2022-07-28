from __future__ import annotations
from typing import Optional, Union, Type

import re
import logging
import asyncio
import inspect
from aiohttp import ClientSession

import spotipy2.types as types
from spotipy2.auth import ClientCredentialsFlow, OauthFlow
from spotipy2.methods import Methods
from spotipy2.exceptions import SpotifyException


class Spotify(Methods):
    API_URL = "https://api.spotify.com/v1/"

    def __init__(
        self,
        auth_flow: Union[ClientCredentialsFlow, OauthFlow],
        mongodb_uri: Optional[str] = None,
        auto_conversion: bool = True,
        recursive_conversion: bool = True,
        *args,
        **kwargs,
    ) -> None:
        self.auth_flow = auth_flow
        self.http = ClientSession(*args, **kwargs)
        self.auto_conversion = auto_conversion
        self.recursive_conversion = recursive_conversion

        if mongodb_uri:
            from pymongo import MongoClient

            match = re.match(r"(mongodb:\/\/\S+\/)(\w+)(\?\S+)?", mongodb_uri)

            if match:
                db_url, db_name, db_params = match.groups()
            else:
                raise Exception("MongoDB URI Not valid")

            db = MongoClient(db_url + (db_params or ""))
            self.cache = db[db_name].spotipy2
        else:
            self.cache = None

    async def _req(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        can_be_cached: bool = False,
    ) -> dict:
        cache_enabled = self.cache is not None and can_be_cached

        # Get cached element
        if cache_enabled:
            doc = self.cache.find_one({"_endpoint": endpoint})
            if doc:
                doc.pop("_endpoint")
                doc.pop("_id")
                return self.convert(doc) if self.auto_conversion else doc

        token = await self.auth_flow.get_access_token(self.http)
        headers = {"Authorization": f"Bearer {token.access_token}"}

        async with self.http.request(
            method, f"{self.API_URL}{endpoint}", params=params, headers=headers
        ) as r:
            json = await r.json()

            try:
                assert r.status == 200
            except AssertionError:
                raise SpotifyException(
                    json["error"]["status"], json["error"]["message"]
                )
            else:
                # Save in cache if enabled
                if cache_enabled:
                    asyncio.create_task(self.cache_resource(endpoint, json))

                return self.convert(json) if self.auto_conversion else json

    async def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        # Check if cache is enabled and request is a simple get [resource]
        can_be_cached = self.cache is not None and (
            params is None
            and re.match(r"^(?!me|browse)([\w-]+)\/(\w+)$", endpoint) is not None
        )

        return await self._req("GET", endpoint, params, can_be_cached)

    async def stop(self) -> None:
        await self.http.close()

    async def __aenter__(self) -> Spotify:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.stop()

    async def cache_resource(self, endpoint, value) -> None:
        try:
            # Insert endpoint for future requests
            value["_endpoint"] = endpoint
            self.cache.insert_one(value)
        except Exception as e:
            logging.warning(f"Can't insert cached object: {e}")

    def convert(self, json: str, recursive: Optional[bool] = None):
        if recursive is None:
            recursive = self.recursive_conversion

        # Find and convert sub-items (recursive by default)
        if recursive:
            list_args = json.items() if isinstance(json, dict) else enumerate(json)
            convertible_args = {
                k: v for k, v in list_args if self._valid_to_convert(v)
            }

            converted_args = {
                k: (
                    (
                        self.convert(v)
                        if isinstance(v, dict) else
                        [self.convert(x) for x in v]
                    )
                ) for k, v in convertible_args.items()
            }

            # Merge with main JSON
            json = {**json, **converted_args}

        # Convert the main item, if possible
        spo_class = self._find_matching_class(json)

        if spo_class:
            return spo_class.from_dict(json)

        return json

    def _valid_to_convert(self, arg: Union[dict, list]) -> bool:
        if isinstance(arg, dict):
            return (
                arg.get("type") in types.SPOTIFY
                or arg.get("items")
                or self._find_matching_class(arg)
            )
        elif isinstance(arg, list):
            return all(self._valid_to_convert(v) for v in arg)
        else:
            return False

    def _find_matching_class(self, json: str) -> Optional[Type[types.BaseType]]:
        # Find matching class if possible, else try brute-forcing it
        spotify_json_type = json.get("type")
        if spotify_json_type in types.SPOTIFY.keys():
            possible_classes = [types.SPOTIFY.get(spotify_json_type)]
        else:
            possible_classes = [
                eval(f"types.{spo_class}") for spo_class in types.__all__[1:]
            ]

        # For each class, find if all JSON keys are in the class parameters
        for possible_class in possible_classes:
            class_args = inspect.signature(possible_class).parameters.items()
            if all(k in json or v.default is None for k, v in class_args):
                return possible_class
        else:
            return None
