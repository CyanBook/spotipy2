from aiohttp import ClientSession

from spotipy2.auth import ClientCredentialsFlow
from spotipy2.methods import Methods
from spotipy2.exceptions import SpotifyException


class Spotify(Methods):
    def __init__(
        self,
        auth_flow: ClientCredentialsFlow,
        *args,
        **kwargs
    ):
        self.auth_flow = auth_flow
        self.http = ClientSession(*args, **kwargs)

    async def stop(self):
        await self.http.close()

    async def _req(self, method, endpoint, params=None) -> dict:
        API_URL = "https://api.spotify.com/v1/"
        token = await self.auth_flow.get_access_token(self.http)
        headers = {"Authorization": f"Bearer {token.access_token}"}

        async with self.http.request(
            method,
            f"{API_URL}{endpoint}",
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

    async def _get(self, endpoint, params=None):
        return await self._req("GET", endpoint, params)
