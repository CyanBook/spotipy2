# Authorization
To have the end user approve your app for access to their Spotify data and features, or to have your app fetch data from Spotify, you need to authorize your application. This section provides all the info you need to authenticate your Spotify client.

!!! info
    They all must be set as `auth_flow` parameter in the `Spotify` class, and they are all subclasses of `BaseAuth`

## Authorization Flows
In the Spotify API, there are different ways to get authorized, called [Authorization Flows](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-flows).

Each flow has a different route to get to the end result, the **access token**, used to make authenticated requests.
For example [`ClientCredentialsFlow`](authorization-flows/client-credentials-flow.md) only requires `client_id` and `client_secret`, while `OauthFlow` requires an explicit consent from the user involved.

## Authenticated Requests
For authenticating, each request contains an **access token**, which is stored in the `token` attribute in the authentication flow class used. It's a [`Token`](token.md) object, which stores every info about the token obtained previously.

## How to use it
First, import one of the authorization flows from `spotipy2.auth`, then set an initialized class of it as `auth_flow` parameter in the `Spotify` 

***

Select the authentication method you need from the list and start your journey!