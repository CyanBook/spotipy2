from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass

from spotipy2 import types


@dataclass
class PlaylistItem(types.BaseType):
    added_at: datetime
    added_by: dict
    is_local: bool
    track: types.Track
    video_thumbnail: dict

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"PlaylistItem(track='{self.track.name}')"
