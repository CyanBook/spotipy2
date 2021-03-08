from __future__ import annotations
from typing import List

import spotipy2
from spotipy2.types import Track


class TrackMethods:
    async def get_tracks(
        self: spotipy2.Spotify,
        track_ids: List[str]
    ) -> List[Track]:
        tracks = await self._get(
            "tracks",
            params={"ids": ",".join([self.get_id(i) for i in track_ids])}
        )
        return [Track.from_dict(track) for track in tracks["tracks"]]

    async def get_track(self: spotipy2.Spotify, track_id: str) -> Track:
        return Track.from_dict(
            await self._get(f"tracks/{self.get_id(track_id)}")
        )
