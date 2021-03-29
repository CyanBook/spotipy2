from __future__ import annotations
from typing import List

from spotipy2 import types


class SimplifiedAlbum(types.BaseType):
    def __init__(
        self,
        album_type: str,
        artists: List[dict],
        available_markets: List[str],
        external_urls,
        href: str,
        id: str,
        images: List[dict],
        name: str,
        release_date: str,
        release_date_precision: str,
        type: str,
        uri: str,
        album_group: str = None,
        **kwargs
    ):
        self.album_group = album_group
        self.album_type = album_type
        self.artists = [types.SimplifiedArtist.from_dict(a) for a in artists]
        self.available_markets = available_markets
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.images = images
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.type = type
        self.uri = uri

    @classmethod
    def from_dict(cls, d: dict) -> SimplifiedAlbum:
        return cls(**d)
