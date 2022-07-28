from __future__ import annotations
from typing import Optional, List
from dataclasses import dataclass, field

from spotipy2 import types


@dataclass
class Track(types.BaseType):
    artists: List[types.Artist]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: dict
    href: str
    id: str
    is_local: bool
    name: str
    track_number: int
    uri: str

    album: Optional[types.Album] = field(default=None)
    external_ids: Optional[dict] = field(default=None)
    popularity: Optional[int] = field(default=None)
    is_playable: Optional[bool] = field(default=None)
    preview_url: Optional[str] = field(default=None)
    available_markets: Optional[List[str]] = field(default=None)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Track(name='{self.name}', id='{self.id}')"
