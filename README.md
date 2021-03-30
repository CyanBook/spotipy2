<p align="center">
    <a href="https://github.com/cyanbook/spotipy2">
        <img src="https://svgshare.com/i/STC.svg" alt="Spotipy2">
    </a>
    <br>
    <b>The next generation Spotify Web API wrapper for Python</b>
    <br>
    <a href="https://spotipy2.org">
        Documentation
    </a>
    •
    <a href="https://github.com/cyanbook/spotipy2/releases">
        Releases
    </a>
    •
    <a href="https://github.com/CyanBook/spotipy2/discussions">
        Community
    </a>
</p>

### Quick example
```python
import asyncio
from spotipy2 import Spotify
from spotipy2.auth import ClientCredentialsFlow

client = Spotify(
    ClientCredentialsFlow(
        client_id="client_id",
        client_secret="client_secret"
    )
)

async def get_track_name(track_id):
    async with client as s:
        track = await s.get_track(track_id)
        print(f"The name of the track is {track.name}")

asyncio.run(get_track_name(input("Insert the track ID: ")))
```

### Features
Well, Spotipy2 has some big advantages over Spotipy.
- **Easy**: You can install spotipy2 with pip and start in minutes to build your code.
- **Fast**: Thanks to [`aiohttp`](https://github.com/aio-libs/aiohttp) speed, spotipy2 is incredibly fast
- **Documented**: API methods, types and public interfaces are all well documented
- **Asynchronous**: You can use this library in an async project without having to 
- **Type-hinted**: All the methods and types are type-hinted, enabling excellent IDE support
- **Types for each [Spotify Object](https://developer.spotify.com/documentation/web-api/reference/#objects-index)**: Each object has its own Type (Class), allowing for simpler development

### Requirements
- Python 3.7 or higher
- A Spotify client ID and secret.

### Installation
```bash
pip install spotipy2
```

## Copyright & License
- Copyright (C) 2020-2021 CyanBook <https://github.com/cyanbook>
- Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](LICENSE)
