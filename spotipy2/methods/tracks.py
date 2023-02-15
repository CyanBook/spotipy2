from __future__ import annotations
from typing import List, Optional

import spotipy2
from spotipy2.types import Track


class TrackMethods:
    async def get_tracks(
        self: spotipy2.Spotify, track_ids: List[str]  # type: ignore
    ) -> List[Track]:
        r = await self._get(
            "tracks", params={"ids": ",".join([self.get_id(i) for i in track_ids])}
        )

        return r["tracks"]

    async def get_track(self: spotipy2.Spotify, track_id: str) -> Track:  # type: ignore
        return await self._get(f"tracks/{self.get_id(track_id)}")

    async def get_recommendations(
        self: spotipy2.Spotify,
        artist_ids: Optional[List[str]] = None,
        track_ids: Optional[List[str]] = None,
        genre_names: Optional[List[str]] = None,
        limit: Optional[int] = None,
        market: Optional[str] = None,
        **kwargs,
    ) -> List[Track]:
        """Returns recommended tracks based on given artist, track or genre seeds.
        Note the names in `genres_names` have to be one of availabe genres accessible
        via the `get_recommendation_genres` function
        #### Keyword arguments:
          - `min/max/target_<attribute>` - For the tuneable track
                    attributes listed in the documentation, these values
                    provide filters and targeting on results.
        """
        assert any(
            [artist_ids, track_ids, genre_names]
        ), "You have to specify at least one seed to get recommendations based on"

        # Mering with `kwargs` to include the tuneable attributes as well
        params = {**self.wrapper(market=market, limit=limit), **kwargs}

        if artist_ids:
            params["seed_artists"] = ",".join(list(map(self.get_id, artist_ids)))
        if track_ids:
            params["seed_tracks"] = ",".join(list(map(self.get_id, track_ids)))
        if genre_names:
            params["seed_genres"] = ",".join(genre_names)

        r = await self._get("recommendations", params)
        return r["tracks"]

    async def get_recommendation_genres(self: spotipy2.Spotify) -> List[str]:
        """Returns a list of genre names to be used as `genre_names`
        argument of the `get_recommendations` function
        """
        r = await self._get("recommendations/available-genre-seeds")
        return r["genres"]
