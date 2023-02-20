from __future__ import annotations
from typing import List, Optional, Union, Dict

import spotipy2
from spotipy2.types import Paging, Album, Artist, Playlist, Track


class SearchMethods:
    SEARCH_TYPES_SUPPORTED = [Album, Artist, Playlist, Track]

    async def search(
        self: spotipy2.Spotify,  # type: ignore
        query: str,
        types: Union[SEARCH_TYPES_SUPPORTED, List[SEARCH_TYPES_SUPPORTED]],
        market: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        include_external: Optional[str] = None,
    ) -> Union[Paging, Dict[Paging]]:
        types = types if isinstance(types, list) else [types]

        params = self.wrapper(
            market=market, limit=limit, offset=offset, include_external=include_external
        )

        
        r = await self._get(
            "search",
            params={
                **{"query": query, "type": ",".join(t.__name__.lower() for t in types)},
                **params,
            },
        )

        if len(r) == 1:
            return next(iter(r.values()))

        return r
