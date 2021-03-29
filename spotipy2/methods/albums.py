from __future__ import annotations
from typing import List, Optional

import spotipy2
from spotipy2.types import Album, Track


class AlbumMethods:
    async def get_albums(
        self: spotipy2.Spotify,
        album_ids: List[str]
    ) -> List[Album]:
        albums = await self._get(
            "albums",
            params={"ids": ",".join([self.get_id(i) for i in album_ids])}
        )
        return [Album.from_dict(a) for a in albums["albums"]]

    async def get_album(self: spotipy2.Spotify, album_id: str) -> Album:
        return Album.from_dict(
            await self._get(f"albums/{self.get_id(album_id)}")
        )

    async def get_album_tracks(
        self: spotipy2.Spotify,
        album_id: str,
        market: Optional[str] = None,
        limit: int = None,
        offset: int = None
    ) -> List[Track]:
        params = self.wrapper(market=market, limit=limit, offset=offset)

        album_tracks = await self._get(
            f"albums/{self.get_id(album_id)}/tracks", params=params
        )
        return [Track.from_dict(track) for track in album_tracks["items"]]
