from __future__ import annotations
from typing import List

import spotipy2
from spotipy2.types import Artist, SimplifiedAlbum, Track


class ArtistMethods:
    async def get_artists(
        self: spotipy2.Spotify,
        artist_ids: List[str]
    ) -> List[Artist]:
        artists = await self._get(
            "artists",
            params={"ids": ",".join([self.get_id(i) for i in artist_ids])}
        )
        return [Artist.from_dict(a) for a in artists["artists"]]

    async def get_artist(self: spotipy2.Spotify, artist_id: str) -> Artist:
        return Artist.from_dict(
            await self._get(f"artists/{self.get_id(artist_id)}")
        )

    async def get_artist_top_tracks(
        self: spotipy2.Spotify, artist_id: str, market: str
    ) -> List[Track]:
        top_tracks = await self._get(
            f"artists/{self.get_id(artist_id)}/top-tracks",
            params={"market": market}
        )
        return [Track.from_dict(track) for track in top_tracks["tracks"]]

    async def get_artist_albums(
        self: spotipy2.Spotify,
        artist_id: str,
        include_groups: str = None,
        market: str = None,
        limit: int = None,
        offset: int = None
    ) -> List[SimplifiedAlbum]:
        params = self.wrapper(
            include_groups=include_groups,
            market=market,
            limit=limit,
            offset=offset
        )

        artist_albums = await self._get(
            f"artists/{self.get_id(artist_id)}/albums", params=params
        )
        return [SimplifiedAlbum.from_dict(a) for a in artist_albums["items"]]
