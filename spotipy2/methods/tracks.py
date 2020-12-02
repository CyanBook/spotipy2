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
            params={"ids": ",".join(track_ids)}
        )

        return [await Track.from_dict(track) for track in tracks["tracks"]]

    async def get_track(self: spotipy2.Spotify, track_id: str) -> Track:
        return await Track.from_dict(await self._get(f"tracks/{track_id}"))
