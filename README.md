<p align="center">
    <a href="https://github.com/cyanbook/spotipy2">
        <img src="https://svgshare.com/i/STC.svg" alt="Spotipy2">
    </a>
    <br>
    <b>The next generation Spotify Web API wrapper for Python 3.7+</b>
    <br>
    <a href="https://spotipy2.org">
        Documentation
    </a>
    •
    <a href="https://github.com/cyanbook/spotipy2/releases">
        Releases
    </a>
    •
    <a href="https://t.me/spotipy2">
        Community
    </a>
</p>

## Installation
```bash
pip install git+https://github.com/CyanBook/spotipy2
```

## Why not spotipy?
Well, Spotipy2 has some big advantages over Spotipy.

### Async support
The entire library is async-only, that translates in less overhead for supporting both sync and async code.

Spotipy2 uses [aiohttp](https://github.com/aio-libs/aiohttp) to make async HTTP requests and every function is async from the ground *(even the ones that doesn't need it)*, giving all the benefits of it.

### 100% Type hinting
Unlike Spotipy, Spotipy2's types and methods are 100% hinted.

Although it's not mandatory, it speeds up the development and allows for excellent IDE support (auto-completion, warnings in case of wrong type usages, and more...).

### A class for each objects 
Spotify2 has a custom class for each [Spotify object](https://developer.spotify.com/documentation/web-api/reference/object-model).

This permits easier understanding of what you're doing, code more readable and maintainable, bound methods, and more.

## Quick example
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

## Copyright & License
- Copyright (C) 2020 CyanBook <https://github.com/cyanbook>
- Licensed under the terms of the GNU Lesser General Public License v3 or later (LGPLv3+)
