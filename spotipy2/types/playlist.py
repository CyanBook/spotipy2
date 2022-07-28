from __future__ import annotations
from typing import List
from dataclasses import dataclass

from spotipy2 import types


@dataclass
class Playlist(types.BaseType):
    collaborative: bool
    description: str
    external_urls: dict
    followers: dict
    href: str
    id: str
    images: List[dict]
    name: str
    owner: dict
    public: bool
    snapshot_id: str
    tracks: List[types.Track]
    uri: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Playlist(name='{self.name}', id='{self.id}')"
