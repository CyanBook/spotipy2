from __future__ import annotations
from typing import List


class Artist:
    def __init__(
        self,
        external_urls: dict,
        followers: dict,
        genres: List[str],
        href: str,
        id: str,
        images: List[dict],
        name: str,
        popularity: int,
        type: str,
        uri: str,
        **kwargs
    ):
        self.external_urls = external_urls
        self.followers = followers
        self.genres = genres
        self.href = href
        self.id = id
        self.images = images
        self.name = name
        self.popularity = popularity
        self.type = type
        self.uri = uri

    @classmethod
    def from_dict(cls, d: dict) -> Artist:
        return cls(**d)
