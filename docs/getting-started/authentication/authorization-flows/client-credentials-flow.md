# Client Credentials Flow
> The Client Credentials flow is used in server-to-server authentication. Only endpoints that do not access user information can be accessed. The advantage here in comparison with requests to the Web API made without an access token, is that a higher rate limit is applied.

You can authenticate via [Client Credentials Flow](https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow) using the `ClientCredentialsFlow` class. Since you don't need any user authorization, you just have to initialize the class to start using it, compared to user-based authentication flows.

#### Parameters

- client_id (`str`) - The Spotify application's Client ID
- client_secret (`str`) - The Spotify application's Client secret
- token (`Token`, *optional*) - A token you already got

#### Example usage

```python
import asyncio
from spotipy2 import Spotify
from spotipy2.auth import ClientCredentialsFlow


# Print an artist's popularity score
async def print_populairty_score(artist_id):
    # Authenticate using ClientCredentialsFlow
    spo_client = Spotify(
        ClientCredentialsFlow(
            client_id="client_id",
            client_secret="client_secret"
        )
    )

    # Use the Spotify client to get artist's info
    async with spo_client as s:
        artist = await s.get_artist(artist_id)
        print(f"{artist.name}'s popularity score is {artist.popularity}/100")

# Print Ed Sheeran's popularity score
asyncio.run(print_populairty_score("6eUKZXaKkcviH0Ku9w2n3V"))
```