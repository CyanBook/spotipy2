from __future__ import annotations
from typing import AsyncGenerator, Optional

import spotipy2
from spotipy2.types import Playlist, Paging, PlaylistItem


class PlaylistMethods:
    async def get_playlist(
        self: spotipy2.Spotify, playlist_id: str  # type: ignore
    ) -> Playlist:
        return await self._get(f"playlists/{self.get_id(playlist_id)}")

    async def get_playlist_tracks(
        self: spotipy2.Spotify,  # type: ignore
        playlist_id: str,
        market: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Paging:
        params = self.wrapper(market=market, limit=limit, offset=offset)

        playlist_tracks = await self._get(
            f"playlists/{self.get_id(playlist_id)}/tracks", params=params
        )

        return playlist_tracks

    async def iter_playlist_tracks(
        self: spotipy2.Spotify,  # type: ignore
        playlist_id: str,
        market: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> AsyncGenerator[PlaylistItem]:
        while True:
            playlist_tracks = await self.get_playlist_tracks(
                playlist_id,
                market=market,
                limit=limit,
                offset=offset
            )

            for track in playlist_tracks.items:
                yield track

            offset += len(playlist_tracks.items)

            if not playlist_tracks.next:
                break
