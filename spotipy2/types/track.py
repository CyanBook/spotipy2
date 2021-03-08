from __future__ import annotations
from typing import Optional, List

from spotipy2.types import SimplifiedArtist


class Track:
    def __init__(
        self,
        album,
        artists,
        disc_number: int,
        duration_ms: int,
        explicit: bool,
        external_ids,
        external_urls,
        href: str,
        id: str,
        is_local: bool,
        name: str,
        popularity: int,
        preview_url: str,
        track_number: int,
        type: str,
        uri: str,
        available_markets: Optional[List[str]] = None,
        is_playable: bool = None,
        linked_from: bool = None,
        restrictions: dict = None,
        **kwargs
    ):
        self.album = album
        self.artists = [SimplifiedArtist.from_dict(a) for a in artists]
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
        self.is_playable = is_playable
        self.linked_from = linked_from
        self.restrictions = restrictions

    @classmethod
    def from_dict(cls, d: dict) -> Track:
        return cls(**d)
