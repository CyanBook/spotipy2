from __future__ import annotations
from typing import Optional
from aiohttp import ClientSession

from spotipy2.auth import ClientCredentialsFlow
from spotipy2.methods import Methods
from spotipy2.exceptions import SpotifyException


class Spotify(Methods):
    API_URL = "https://api.spotify.com/v1/"

    def __init__(
        self,
        auth_flow: ClientCredentialsFlow,
        *args,
        **kwargs
    ) -> None:
        self.auth_flow = auth_flow
        self.http = ClientSession(*args, **kwargs)

    async def _req(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None
    ) -> dict:
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
                return json

    async def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        return await self._req("GET", endpoint, params)

    async def stop(self) -> None:
        await self.http.close()

    async def __aenter__(self) -> Spotify:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.stop()
