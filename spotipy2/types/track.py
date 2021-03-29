from __future__ import annotations
from typing import Optional, List

from spotipy2 import types


class Track(types.BaseType):
    def __init__(
        self,
        artists: List[dict],
        disc_number: int,
        duration_ms: int,
        explicit: bool,
        external_urls,
        href: str,
        id: str,
        is_local: bool,
        name: str,
        preview_url: str,
        track_number: int,
        type: str,
        uri: str,
        album: dict = None,
        external_ids: dict = None,
        popularity: int = None,
        available_markets: Optional[List[str]] = None,
        **kwargs
    ):
        self.album = types.SimplifiedAlbum.from_dict(album) if album else None
        self.artists = [types.SimplifiedArtist.from_dict(a) for a in artists]
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_ids = external_ids
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.is_local = is_local
        self.name = name
        self.popularity = popularity
        self.preview_url = preview_url
        self.track_number = track_number
        self.type = type
        self.uri = uri

    @classmethod
    def from_dict(cls, d: dict) -> Track:
        return cls(**d)
