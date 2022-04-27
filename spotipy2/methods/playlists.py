from __future__ import annotations
from typing import AsyncGenerator, List, Optional

import spotipy2
from spotipy2.types import Playlist, Track


class PlaylistMethods:
    async def get_playlist(
        self: spotipy2.Spotify, playlist_id: str  # type: ignore
    ) -> Playlist:
        return Playlist.from_dict(
            await self._get(f"playlists/{self.get_id(playlist_id)}")
        )

    async def get_playlist_tracks(
        self: spotipy2.Spotify, # type: ignore
        playlist_id: str,
        market: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Track]:
        params = self.wrapper(market=market, limit=limit, offset=offset)

        playlist_tracks = await self._get(
            f"playlists/{self.get_id(playlist_id)}/tracks", params=params
        )

        return [Track.from_dict(track["track"]) for track in playlist_tracks["items"]]

    async def iter_playlist_tracks(
        self: spotipy2.Spotify, # type: ignore
        playlist_id: str,
        market: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> AsyncGenerator[Track, None]:
        while True:
            params = self.wrapper(market=market, limit=limit, offset=offset)

            playlist_tracks = await self._get(
                f"playlists/{self.get_id(playlist_id)}/tracks", params=params
            )

            for track in playlist_tracks["items"]:
                yield Track.from_dict(track["track"])

            offset += len(playlist_tracks["items"])

            if not playlist_tracks["next"]:
                return
