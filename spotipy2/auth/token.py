from __future__ import annotations
from typing import Optional
from datetime import datetime, timedelta


class Token:
    def __init__(
        self,
        access_token: str,
        token_type: str,
        scope: str,
        expires_in: int,
        refresh_token: Optional[str] = None
    ) -> None:
        self.access_token = access_token
        self.token_type = token_type
        self.scope = scope
        self.expires_in = expires_in
        self.expires_at = datetime.now() + timedelta(seconds=self.expires_in)
        self.refresh_token = refresh_token

    @classmethod
    async def from_dict(cls, d: dict) -> Token:
        return cls(**d)
