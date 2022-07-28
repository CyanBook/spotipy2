from __future__ import annotations
from typing import List, Optional, Union, Dict

import spotipy2
from spotipy2.types import Paging, Album, Artist, Playlist, Track


class SearchMethods:
    TYPES_SUPPORTED = [Album, Artist, Playlist, Track]

    async def search(
        self: spotipy2.Spotify,  # type: ignore
        query: str,
        types: Union[TYPES_SUPPORTED, List[TYPES_SUPPORTED]],
        market: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        include_external: Optional[str] = None,
    ) -> Union[Paging, Dict[Paging]]:
        types = types if isinstance(types, list) else [types]

        params = self.wrapper(
            market=market, limit=limit, offset=offset, include_external=include_external
        )

        return await self._get(
            "search",
            params={
                **{"query": query, "type": ",".join(t.__name__.lower() for t in types)},
                **params,
            },
        )
