from __future__ import annotations
from typing import List, Union, Dict, Type

import spotipy2
from spotipy2.types import Artist, Album, SimplifiedAlbum, Track


class SearchMethods:
    TYPES_SUPPORTED = Union[Artist, Album, Track]
    TYPES_RETURNED = Union[Artist, SimplifiedAlbum, Track]

    async def search(
        self: spotipy2.Spotify,
        query: str,
        types: Union[Type[TYPES_SUPPORTED], List[Type[TYPES_SUPPORTED]]],
        market: str = None,
        limit: int = None,
        offset: int = None,
        include_external: str = None
    ) -> Union[List[TYPES_RETURNED], Dict[str, TYPES_RETURNED]]:
        params = self.wrapper(
            market=market,
            limit=limit,
            offset=offset,
            include_external=include_external
        )

        unique_types = set()
        for t in ([types] if not isinstance(types, list) else types):
            unique_types.add(
                t.__name__.lower() if not isinstance(
                    t, SimplifiedAlbum
                ) else "album"
            )

        items = await self._get(
            "search",
            params={
                **{"query": query, "type": ','.join(t for t in unique_types)},
                **params
            }
        )

        results = {} if len(unique_types) > 1 else []
        for k, v in items.items():
            if k == "artists":
                c = Artist
            elif k == "albums":
                c = SimplifiedAlbum
            elif k == "tracks":
                c = Track
            else:
                raise ValueError("No class valid")

            tr = [c.from_dict(i) for i in v["items"]]
            if len(unique_types) > 1:
                results[k] = tr
            else:
                results = tr

        return results
