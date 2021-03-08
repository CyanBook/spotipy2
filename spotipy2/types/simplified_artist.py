from __future__ import annotations


class SimplifiedArtist:
    def __init__(
        self,
        external_urls: dict,
        href: str,
        id: str,
        name: str,
        type: str,
        uri: str,
        **kwargs
    ):
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.name = name
        self.type = type
        self.uri = uri

    @classmethod
    def from_dict(cls, d: dict) -> SimplifiedArtist:
        return cls(**d)
