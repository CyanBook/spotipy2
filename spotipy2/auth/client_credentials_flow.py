from typing import Optional
from aiohttp import ClientSession
from datetime import datetime, timezone

from .base_auth_flow import BaseAuthFlow
from .token import Token


class ClientCredentialsFlow(BaseAuthFlow):
    def __init__(
        self, client_id: str, client_secret: str, token: Optional[Token] = None
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

    async def get_access_token(self, http: ClientSession) -> Token:
        API_URL = "https://accounts.spotify.com/api/token"
        GRANT_TYPE = {"grant_type": "client_credentials"}

        if self.token and self.token.expires_at > datetime.now(timezone.utc):
            return self.token

        async with http.post(
            API_URL, data=GRANT_TYPE, headers=self.make_auth_header()
        ) as r:
            return await Token.from_dict(await r.json())
