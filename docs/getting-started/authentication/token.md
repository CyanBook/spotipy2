# Token
The obtained token and its related info.

The `Token` class is a wrapper for storing token information, like access token, refresh token, expiration time, scopes, and more. It simplifies the way token info is stored and lets a simpler way to access its parameter compared to a dict. 

#### Parameters

- access_token (`str`) - An access token that can be provided in subsequent calls
- token_type (`str`) - How the access token may be used: always "Bearer"
- scopes (List of `str`) - A list of [scopes](https://developer.spotify.com/documentation/general/guides/scopes/) granted for this access_token
- expires_in (`int`) - The time period in seconds for which the access token is valid.
- expires_at ([`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)) - A datetime object that points to the access token's expiration date
- refresh_token (`str`, *optional*) - A token that can be sent to regenerate a new `access_token`