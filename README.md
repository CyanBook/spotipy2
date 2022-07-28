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

async def get_track_name(track_id):
    client = Spotify(
        ClientCredentialsFlow(
            client_id="client_id",
            client_secret="client_secret"
        )
    )

    async with client as s:
        track = await s.get_track(track_id)
        print(f"The name of the track is {track.name}")

asyncio.run(get_track_name(input("Insert the track ID: ")))
```

### Key Features
- **Easy** - Makes the Spotify API easy to understand and intuitive, without giving less customization.
- **Fast** - Thanks to its async design and [`aiohttp`](https://github.com/aio-libs/aiohttp) speed, spotipy2 is incredibly fast
- **Type-hinted** - All the methods and types are type-hinted, enabling excellent IDE support
- **Documented** - API methods, types and interfaces are all well documented

### Installing
```bash
pip install spotipy2
```

## Resources
- Check out the docs at https://spotipy2.org to learn about Spotipy2.
- For any issue, open one [here](https://github.com/CyanBook/spotipy2/issues) or contact me privately via [Telegram](https://t.me/CyanBook).
- If you have anything else to ask, feel free to open a [discussion](https://github.com/CyanBook/spotipy2/discussions)