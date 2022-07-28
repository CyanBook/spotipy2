from .base import BaseType
from .paging import Paging
from .album import Album
from .artist import Artist
from .playlist import Playlist
from .track import Track
from .user import User
from .playlist_item import PlaylistItem

SPOTIFY = {
    "album": Album,
    "artist": Artist,
    "playlist": Playlist,
    "track": Track,
    "user": User
}

__all__ = [
    "BaseType",
    "Paging",
    "Album",
    "Artist",
    "Playlist",
    "Track",
    "User",
    "PlaylistItem"
]
