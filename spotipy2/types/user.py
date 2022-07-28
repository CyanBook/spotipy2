from __future__ import annotations
from dataclasses import dataclass, field

from spotipy2 import types


@dataclass
class User(types.BaseType):
    href: str
    id: str
    uri: str

    display_name: str = field(default=None)
    external_urls: dict = field(default=None)
    followers: dict = field(default=None)
    images: dict = field(default=None)

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        if self.display_name:
            return f"User(display_name='{self.display_name}', id='{self.id}')"
        else:
            return f"User(id='{self.id}')"
