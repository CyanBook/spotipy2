from aiohttp import ClientSession

from spotipy2.auth import ClientCredentialsFlow


class Spotify:
    def __init__(
        self,
        auth_flow: ClientCredentialsFlow
    ):
        self.auth_flow = auth_flow
        self.http = ClientSession()

    async def stop(self):
        await self.http.close()

    async def _req(self, method, endpoint) -> dict:
        API_URL = "https://api.spotify.com/v1/"
        token = await self.auth_flow.get_access_token(self.http)
        headers = {"Authorization": f"Bearer {token.access_token}"}

        async with self.http.request(
            method,
            f"{API_URL}{endpoint}",
            headers=headers
        ) as r:
            return await r.json()

    async def _get(self, endpoint):
        return await self._req("GET", endpoint)
