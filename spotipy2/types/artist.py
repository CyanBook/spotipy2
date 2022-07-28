from __future__ import annotations
from typing import List
from dataclasses import dataclass, field

from spotipy2 import types


@dataclass
class Artist(types.BaseType):
    external_urls: dict
    href: str
    id: str
    name: str
    uri: str

    followers: dict = field(default=None)
    genres: List[str] = field(default=None)
    images: List[dict] = field(default=None)
    popularity: int = field(default=None)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Artist(name='{self.name}', id='{self.id}')"
