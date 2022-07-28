from __future__ import annotations
from typing import List, Optional, Type
from dataclasses import dataclass

from spotipy2 import types


@dataclass
class Paging(types.BaseType):
    href: str
    items: List[Type[types.BaseType]]
    limit: int
    next: Optional[str]
    offset: int
    previous: Optional[str]
    total: int

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Paging(len(items)={len(self.items)}, limit={self.limit}, offset={self.offset}, total={self.total})"
