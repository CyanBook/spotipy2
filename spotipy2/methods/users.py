from __future__ import annotations
import spotipy2
from spotipy2.types import User


class UserMethods:
    async def get_current_user(self: spotipy2.Spotify) -> User:  # type: ignore
        return await self._get("me")
