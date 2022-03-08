from __future__ import annotations
from typing import List

from spotipy2 import types


class Playlist(types.BaseType):
    def __init__(
        self,
        collaborative: bool,
        description: str,
        external_urls: dict,
        followers: dict,
        href: str,
        id: str,
        images: List[dict],
        name: str,
        owner: dict,
        public: bool,
        snapshot_id: str,
        tracks,
        type: str,
        uri: str,
        **kwargs,
    ):
        self.collaborative = collaborative
        self.description = description
        self.external_urls = external_urls
        self.followers = followers
        self.href = href
        self.id = id
        self.images = images
        self.name = name
        self.owner = owner
        self.public = public
        self.snapshot_id = snapshot_id
        self.tracks = tracks
        self.type = type
        self.uri = uri

    @classmethod
    def from_dict(cls, d: dict) -> Playlist:
        return cls(**d)
