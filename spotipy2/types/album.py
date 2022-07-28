from __future__ import annotations
from typing import Optional, List
from dataclasses import dataclass, field

from spotipy2 import types


@dataclass
class Album(types.BaseType):
    album_type: str
    total_tracks: int
    artists: List[types.Artist]
    external_urls: dict
    href: str
    id: str
    images: List[dict]
    name: str
    release_date: str
    release_date_precision: str
    uri: str

    available_markets: Optional[List[str]] = field(default=None)
    copyrights: List[dict] = field(default=None)
    external_ids: dict = field(default=None)
    genres: List[str] = field(default=None)
    label: str = field(default=None)
    popularity: int = field(default=None)
    tracks: List[types.Track] = field(default=None)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Album(name='{self.name}', id='{self.id}')"
