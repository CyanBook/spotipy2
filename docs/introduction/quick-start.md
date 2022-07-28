# Quick start
The next steps are for a super quick start for starting using this library.

## Get Spotipy2 up and running
1. Install Spotipy2 with ```pip install spotipy2```.
2. Get your client `client_id` and `client_secret` from [here](https://developer.spotify.com/dashboard/applications).
3. Open your favorite editor and copy-paste the following:
```python
import asyncio
from spotipy2 import Spotify
from spotipy2.auth import ClientCredentialsFlow

async def get_track_name(track_id):
    spo_client = Spotify(
        ClientCredentialsFlow(
            client_id="client_id",
            client_secret="client_secret"
        )
    )

    async with spo_client as s:
        track = await s.get_track(track_id)
        print(f"The name of the track is {track.name}")

asyncio.run(get_track_name(input("Insert the track ID: ")))
```
4. Replace `client_id` and `client_secret` with your values.
5. Save the file as `test.py`.
6. Run the script with `python test.py`.
7. Type a Track ID and watch getting its name back!

## Enjoy the api
This was a very basic example, but this library it's capable of doing much more complex things. Take your time to explore the documentation and look at more in-depth examples in the next pages.