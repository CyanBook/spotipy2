from __future__ import annotations
from typing import List

import spotipy2
from spotipy2.types import Artist


class ArtistMethods:
    async def get_artists(
        self: spotipy2.Spotify,
        artist_ids: List[str]
    ) -> List[Artist]:
        artists = await self._get(
            "artists",
            params={"ids": ",".join(artist_ids)}
        )

        return [await Artist.from_dict(track) for track in artists["artists"]]

    async def get_artist(self: spotipy2.Spotify, artist_id: str) -> Artist:
        return await Artist.from_dict(await self._get(f"artists/{artist_id}"))
