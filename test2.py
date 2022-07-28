import asyncio
from spotipy2 import Spotify
from spotipy2.types import Track, Artist
from spotipy2.auth import OauthFlow, ClientCredentialsFlow
import os
import logging
import time

logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.DEBUG
)

spotify_client_id = os.getenv("spotify_client_id")
spotify_client_secret = os.getenv("spotify_client_secret")

flow = OauthFlow(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri="http://localhost:9000",
    scope=["user-read-playback-state"],
    open_browser=True,
    show_dialog=False
)

flow = ClientCredentialsFlow(
    spotify_client_id,
    spotify_client_secret
)

# flow = OauthFlow(
#     client_id=spotify_client_id,
#     client_secret=spotify_client_secret,
#     redirect_uri="http://localhost:9000",
#     scope=["user-read-playback-state"],
#     token="AQBPjFG0yc7AZ9O9xPftsIukrxkxq0FP76hoEPKZ8_LDSMucvjAD_c6MY0De825BeWaOxeuqs2Yvzz_UhHihxRrI_Cb7U4kmhCiNW4JRRUxVGPCjuQCJKVaIPW4ACe_4t8VOJtPbggJiAv2B6HXfkyXRyuZhArGo8Jq-R_fnX57E4IX9S2cPWAXvPy8d93dhpp-h"
# )


async def main():
    client = Spotify(
        flow,
        mongodb_uri="mongodb://localhost:27017/spotipy2"
    )

    start = time.perf_counter()
    async with client as s:
        tracks = ["0KS1D0MaqgqYku6LDj3ekl", "0eu4C55hL6x29mmeAjytzC"]
        albums = ["1mduA9KWQcE64fHeH8U17C", "4kDPKnqhLo9WVqSEjgrv0u"]
        artists = ["5dXlc7MnpaTeUIsHLVe3n4", "3hBQ4zniNdQf1cqqo6hzuW"]

        # track_1 = await s.get_track(tracks[0])
        # artist_top_1 = await s.get_artist_top_tracks(artists[0], market="US")
        album_tracks = await s.get_album_tracks(albums[0])
        search_1 = await s.search(
            "salmo",
            types=[Artist, Track]
        )

        print(album_tracks)
        print(search_1)

        # playlist_tracks = await s.get_playlist_tracks("37ySG0uEdR7PqrGtT0uGyQ")
        # async for p_item in s.iter_playlist_tracks("37ySG0uEdR7PqrGtT0uGyQ"):
        #     print(p_item.added_at)
        #     if p_item.track:
        #         print(p_item.track.name)
        x = 0
        async for p in s.iter_playlist_tracks("13XOQRc3UPiTYVUsVugqdk"):
            if p.track:
                print(p.track.name)

            if x >= 10:
                print("done")
                break
            else:
                x += 1

        track_1 = await s.get_track(tracks[0])
        # track_2 = await s.get_track(tracks[1])
        # tracks_res = await s.get_tracks(tracks)

        album_1 = await s.get_album(albums[0])
        # album_2 = await s.get_album(albums[1])
        # album_tracks_1 = await s.get_album_tracks(albums[0])
        # album_tracks_2 = await s.get_album_tracks(albums[1])
        # albums_res = await s.get_albums(albums)

        artist_1 = await s.get_artist(artists[0])
        # artist_2 = await s.get_artist(artists[1])
        
        #search = await s.search("salmo")
        search_2 = await s.search("salmo", types=Artist)
        search_2 = await s.search("salmo", types=[Track, Artist], market="US")
        artist_top_2 = await s.get_artist_top_tracks(artists[1], market="US")
        artist_albums_1 = await s.get_artist_albums(artists[0])
        artist_albums_2 = await s.get_artist_albums(artists[1])
        artist_res = await s.get_artists(artists)

        playlist_1 = await s.get_playlist("37ySG0uEdR7PqrGtT0uGyQ")


    end = time.perf_counter()
    print(f"DONE - {end-start}")


asyncio.get_event_loop().run_until_complete(main())
