from __future__ import annotations
from typing import Optional

import re
import logging
import asyncio
from aiohttp import ClientSession

from spotipy2.auth import ClientCredentialsFlow
from spotipy2.methods import Methods
from spotipy2.exceptions import SpotifyException


class Spotify(Methods):
    API_URL = "https://api.spotify.com/v1/"

    def __init__(
        self,
        auth_flow: ClientCredentialsFlow,
        mongodb_uri: Optional[str] = None,
        *args,
        **kwargs
    ) -> None:
        self.auth_flow = auth_flow
        self.http = ClientSession(*args, **kwargs)

        if mongodb_uri:
            from pymongo import MongoClient

            match = re.match(
                r"(mongodb:\/\/\S+\/)(\w+)(\?\S+)?",
                mongodb_uri
            )

            if match:
                db_url, db_name, db_params = match.groups()
            else:
                raise Exception("MongoDB URI Not valid")

            db = MongoClient(db_url + (db_params or ""))
            self.cache = db[db_name].spotipy2
            self.is_cache = True
        else:
            self.cache = None
            self.is_cache = False

    async def _req(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        can_be_cached: bool = False
    ) -> dict:
        if self.is_cache and can_be_cached:
            doc = self.cache.find_one({"_endpoint": endpoint})
            if doc:
                doc.pop("_endpoint")
                return doc

        token = await self.auth_flow.get_access_token(self.http)
        headers = {"Authorization": f"Bearer {token.access_token}"}

        async with self.http.request(
            method,
            f"{self.API_URL}{endpoint}",
            params=params,
            headers=headers
        ) as r:
            json = await r.json()

            try:
                assert r.status == 200
            except AssertionError:
                raise SpotifyException(
                    json["error"]["status"],
                    json["error"]["message"]
                )
            else:
                # Cache if possible
                if self.is_cache and can_be_cached:
                    asyncio.create_task(
                        self.cache_resource(endpoint, json)
                    )

                return json

    async def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        # Check if cache is enabled and request is a simple get [resource]
        can_be_cached = self.is_cache and (
            params is None
            and re.match(
                r"^(?!me|browse)([\w-]+)\/(\w+)$",
                endpoint
            ) is not None
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
