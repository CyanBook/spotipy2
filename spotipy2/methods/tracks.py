from __future__ import annotations
from typing import List

import spotipy2
from spotipy2.types import Track


class TrackMethods:
    async def get_tracks(
        self: spotipy2.Spotify, track_ids: List[str]  # type: ignore
    ) -> List[Track]:
        r = await self._get(
            "tracks",
            params={"ids": ",".join([self.get_id(i) for i in track_ids])}
        )

        return r["tracks"]

    async def get_track(self: spotipy2.Spotify, track_id: str) -> Track:  # type: ignore
        return await self._get(f"tracks/{self.get_id(track_id)}")
