from __future__ import annotations
from typing import AsyncGenerator, List, Optional

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

    async def get_current_user_playlists(
        self: spotipy2.Spotify,  # type: ignore,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Paging:
        params = self.wrapper(limit=limit, offset=offset)
        return await self._get("me/playlists", params=params)

    async def create_playlist(
        self: spotipy2.Spotify,  # type: ignore
        user_id: str,
        name: str,
        public: Optional[bool] = None,
        collaborative: Optional[bool] = None,
        description: Optional[str] = None,
    ) -> Playlist:
        body = self.wrapper(
            name=name,
            public=public,
            collaborative=collaborative,
            description=description,
        )
        return await self._post(f"users/{self.get_id(user_id)}/playlists", body=body)


    async def add_items_to_playlist(
        self: spotipy2.Spotify,  # type:ignore
        playlist_id: str,
        uris: List[str],
        position: Optional[int] = None,
    ) -> dict:
        body = self.wrapper(uris=uris, position=position)
        return await self._post(
            f"playlists/{self.get_id(playlist_id)}/tracks", body=body
        )

