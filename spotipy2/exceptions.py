class SpotifyException(Exception):
    """
    General Spotify exception.
    Packs together all the possible errors Spotify could give
    """

    def __init__(self, status: int, message: str) -> None:
        self.status = status
        self.message = message

    def __repr__(self) -> str:
        return '<SpotifyException(status={0}, message="{1}")>'.format(
            self.status, self.message
        )
