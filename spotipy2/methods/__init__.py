import re

from .artists import ArtistMethods
from .tracks import TrackMethods


class Methods(ArtistMethods, TrackMethods):
    @staticmethod
    def get_id(s: str) -> str:
        if m := re.search("(?!.*/).+", s):
            return m[0].split("?")[0]
        else:
            raise ValueError("ID not valid")
