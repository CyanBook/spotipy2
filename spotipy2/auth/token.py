from __future__ import annotations
from typing import Optional
from datetime import datetime, timedelta, timezone


class Token:
    def __init__(
        self,
        access_token: str,
        token_type: str,
        scope: str,
        expires_in: int,
        expires_at: datetime,
        refresh_token: Optional[str] = None
    ) -> None:
        self.access_token = access_token
        self.token_type = token_type
        self.scope = scope
        self.expires_in = expires_in
        self.expires_at = expires_at
        self.refresh_token = refresh_token

    @classmethod
    async def from_dict(cls, d: dict) -> Token:
        expires_at = datetime.now(
            timezone.utc
        ) + timedelta(seconds=d["expires_in"])

        return cls(
            access_token=d["access_token"],
            token_type=d["token_type"],
            scope=d["scope"],
            expires_in=d["expires_in"],
            expires_at=expires_at,
            refresh_token=d["refresh_token"]
        )
