from __future__ import annotations
from typing import List, Optional

import spotipy2
from spotipy2.types import Album
from spotipy2.types.paging import Paging


class AlbumMethods:
    async def get_albums(
        self: spotipy2.Spotify, album_ids: List[str]  # type: ignore
    ) -> List[Album]:
        albums = await self._get(
            "albums", params={"ids": ",".join([self.get_id(i) for i in album_ids])}
        )
        return albums["albums"]

    async def get_album(self: spotipy2.Spotify, album_id: str) -> Album:  # type: ignore
        return await self._get(f"albums/{self.get_id(album_id)}")

    async def get_album_tracks(
        self: spotipy2.Spotify,  # type: ignore
        album_id: str,
        market: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Paging:
        params = self.wrapper(market=market, limit=limit, offset=offset)

        album_tracks = await self._get(
            f"albums/{self.get_id(album_id)}/tracks", params=params
        )
        return album_tracks
