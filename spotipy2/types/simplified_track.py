from __future__ import annotations
from typing import List, Mapping

from spotipy2 import types


class SimplifiedTrack(types.BaseType):
    def __init__(
        self,
        artists: List[dict],
        available_markets: List[str],
        disc_number: int,
        duration_ms: int,
        explicit: bool,
        external_urls,
        href: str,
        id: str,
        is_local: bool,
        is_playable: bool,
        linked_from,
        name: str,
        preview_url: str,
        restrictions,
        track_number: int,
        uri: str,
        **kwargs
    ):
        self.artists = [types.SimplifiedArtist.from_dict(a) for a in artists]
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.is_local = is_local
        self.is_playable = is_playable
        self.linked_from = linked_from
        self.name = name
        self.preview_url = preview_url
        self.restrictions = restrictions
        self.track_number = track_number
        self.uri = uri

    @classmethod
    def from_dict(cls, d: Mapping) -> SimplifiedTrack:
        return cls(**d)
