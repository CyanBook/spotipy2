# Quick start
The next steps are for a super quick start for starting using this library.

## Get Spotipy2 up and running
First, open your favorite text editor, paste this code and save the file:

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

1. Install Spotipy2 as explained [here](/introduction/installation)
2. Replace `client_id` and `client_secret` with your values
3. Start the script
4. Done!