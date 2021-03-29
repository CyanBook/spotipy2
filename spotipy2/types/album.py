from __future__ import annotations
from typing import List

from spotipy2 import types


class Album(types.BaseType):
    def __init__(
        self,
        album_type: str,
        artists: List[types.Artist],
        available_markets: List[str],
        copyrights,
        external_ids,
        external_urls,
        genres: List[str],
        href: str,
        id: str,
        images: List[dict],
        label: str,
        name: str,
        popularity: int,
        release_date: str,
        release_date_precision: str,
        restrictions,
        tracks,
        type: str,
        uri: str,
        **kwargs
    ):
        self.album_type = album_type
        self.artists = artists
        self.available_markets = available_markets
        self.copyrights = copyrights
        self.external_ids = external_ids
        self.external_urls = external_urls
        self.genres = genres
        self.href = href
        self.id = id
        self.images = images
        self.label = label
        self.name = name
        self.popularity = popularity
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.restrictions = restrictions
        self.tracks = tracks
        self.type = type
        self.uri = uri

    @classmethod
    def from_dict(cls, d: dict) -> Album:
        return cls(**d)
