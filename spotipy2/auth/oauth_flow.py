from base64 import b64encode
from typing import Optional, List, Callable
from aiohttp import web, ClientSession
from datetime import datetime, timezone
from pathlib import Path

from .base_auth_flow import BaseAuthFlow
from .token import Token
from ..exceptions import SpotifyException

import urllib.parse
import re
import secrets
import asyncio
import webbrowser


class OauthFlow(BaseAuthFlow):
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            # `scope` and `show_dialog` are None on purpose so that
            # the wrapper method removes them if not given
            scope: Optional[List[str]] = None,
            show_dialog: Optional[bool] = None,
            token: Optional[Token] = None,
            open_browser: bool = False,
            disable_builtin_server: bool = False,
            authenticated_html_response: Optional[str] = Path(__file__).parent / "./static/authenticated.html",
            failed_html_response: Optional[str] = Path(__file__).parent / "./static/failed.html",
            state_verifier: Optional[Callable[[str], bool]] = None
    ) -> None:
        """
        ### Args
        - client_id: `str`, Spotify client id
        - client_secret: `str`, Spotify client secret
        - redirect_uri: `str`, URI for Oauth callback, URI(s) using localhost (127.0.0.1)
        will automatically start spotipy2's built-in server. URI must match one of the URI's on
        the project's Spotify Dashboard character for character.
        - scope: `Optional[List[str]]`, List of Spotify scopes,
        full list: https://developer.spotify.com/documentation/general/guides/authorization/scopes/
        - show_dialog: `Optional[bool]`, Whether to force the user to approve the app again if they have already done so
        - token: `Optional[str]`, The access token
        - open_browser: `bool`, Whether to open the browser or not when get_redirect is called
        - disable_builtin_server: `bool`, If True, the built-in server will not be started
        - authenticated_html_response: `Optional[str]`, The path to a html file which will be displayed if a user is
        successfully authenticated, only works when using spotipy2's built-in server
        - failed_html_response: `Optional[str]`, The path to a html file which will be displayed if a user is
        NOT successfully authenticated, only works when using spotipy2's built-in server
        - state_verifier: `Optional[Callable[[str], bool]]`, Method to be executed to verify state to prevent XSS attack. 

        ### Returns
        - `None`

        ### Errors raised
        - None

        ### Function / Notes
        - For spotipy2's built-in server to start, the redirect_uri must contain localhost as
        the domain as well as the port, eg. http://localhost:9000. No path should be specified and HTTPS cannot be used
        and will be converted to HTTP. If you would like to use HTTPS, consider setting up your own web server.
        In addition, you must call the get_redirect method before executing any requests
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = " ".join(scope) if scope else None
        self.show_dialog = str(show_dialog).lower() if show_dialog is not None else None

        self.token = token
        self.open_browser = open_browser
        self.authenticated_html_response = authenticated_html_response
        self.failed_html_response = failed_html_response
        self.disable_builtin_server = disable_builtin_server
        self.header = self.make_auth_header()

        self.state_verifier = state_verifier if state_verifier else self._state_verifier
        self.expected_state = secrets.token_urlsafe(16)

        self.server = None  # Oauth server
        self.server_runner = None
        self.timeout = 3

    async def get_redirect(self) -> str:
        """
        ### Args
        - None

        ### Returns
        - `str`, The authentication URI which the user must navigate to in order to get authenticated

        ### Errors raised
        - None

        ### Function / Notes
        - This will automatically start spotipy2's built-in server if the redirect_uri contains localhost as
        the domain as well as the port, eg. http://localhost:9000.
        """
        API_URL = "https://accounts.spotify.com/authorize?"

        data = self.wrapper(
            response_type="code",
            client_id=self.client_id,
            scope=self.scope,
            redirect_uri=self.redirect_uri,
            show_dialog=self.show_dialog,
            state=self.expected_state,
        )

        final_url = API_URL + urllib.parse.urlencode(data)

        if not self.disable_builtin_server:
            self.redirect_uri = self.redirect_uri.replace("https://", "http://")
            regex = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
            result = re.search(regex, self.redirect_uri)
            if result.group("host") in ['localhost', '127.0.0.1'] and result.group("port") != '':
                self.server = OauthServer(self.authenticated_html_response,
                                          self.failed_html_response,
                                          self.state_verifier)
                runner = web.AppRunner(self.server)
                await runner.setup()
                self.server_runner = web.TCPSite(runner, 'localhost', int(result.group("port")))
                # We don't need to implement any code for graceful shutdown as we don't do anything such as data
                # streaming
                await self.server_runner.start()
        
        if self.open_browser:
            webbrowser.open_new(final_url)

        return final_url

    async def get_access_token(self, http: ClientSession) -> Token:
        """
        ### Args
        - http: `ClientSession`, Aiohttp ClientSession to use

        ### Returns
        - `Token`, The access token

        ### Errors raised
        - None

        ### Function / Notes
        - None
        """
        if self.token and self.token.expires_at > datetime.now(timezone.utc):
            return self.token
        elif self.token and self.token.expires_at < datetime.now(timezone.utc):
            return await self.refresh_token(http)
        if not self.disable_builtin_server:
            while not self.server.code:
                await asyncio.sleep(self.timeout)
            code = self.server.code
        else:
            url = input("Please paste the URI you were redirected to: ")
            processed_url = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            code = processed_url.get('code')
            state = processed_url.get('state')[0]
            if code:
                if await self._state_verifier(state):
                    code = code[0]
                else:
                    raise RuntimeError(f"State does not match. State: {state}")
            else:
                raise SpotifyException(403, f"Authentication failed. State: {state}")
        self.token = await self._get_access_token(code,
                                                  self.client_id,
                                                  self.client_secret,
                                                  self.redirect_uri,
                                                  http)
        return self.token

    @staticmethod
    async def _get_access_token(token: str, client_id: str, client_secret: str, redirect_uri: str,
                                http: ClientSession) -> Token:
        """
        ### Args
        - token: `str`, 'code' returned from Oauth callback (redirect_uri), this is NOT the access token
        - client_id: `str`, Spotify client id
        - client_secret: `str`, Spotify client secret
        - redirect_uri: `str`, URI for Oauth callback, URI must match one of the URI's on
        the project's Spotify Dashboard character for character
        - http: `ClientSession`, Aiohttp ClientSession to use

        ### Returns
        - `Token`, The access token

        ### Errors raised
        - None

        ### Function / Notes
        - This method is static so that developers who have already gotten the 'code' through their own code (for eg.
        they already have a separate website using flask) can easily use this method and instantiate a new auth
        flow with the access token which is returned
        """

        API_URL = "https://accounts.spotify.com/api/token"
        data = {
            "code": token,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }

        HEADER = {
            "Authorization": "Basic %s"
                             % b64encode(f"{client_id}:{client_secret}".encode()).decode()
        }

        async with http.post(
                API_URL, data=data, headers=HEADER
        ) as r:
            if r.status < 200 or r.status > 299:
                raise SpotifyException(r.status, r.json()) # example: {'error': 'invalid_grant', 'error_description': 'Invalid redirect URI'}
            return await Token.from_dict(await r.json())

    async def refresh_token(self, http: ClientSession) -> Token:
        """
        ### Args
        - http: `ClientSession`, Aiohttp ClientSession to use

        ### Returns
        - `Token`, The access token

        ### Errors raised
        - None

        ### Function / Notes
        - None
        """
        API_URL = "https://accounts.spotify.com/api/token"
        data = {
            "refresh_token": self.token.refresh_token,
            "grant_type": "refresh_token"
        }

        HEADER = self.header

        async with http.post(
                API_URL, data=data, headers=HEADER
        ) as r:
            response = await r.json()
            # Refresh token is not received on token refresh
            response["refresh_token"] = self.token.refresh_token
            self.token = await Token.from_dict(response)
            return self.token

    async def _state_verifier(self, state: str) -> bool:
        """
        ### Args
        - state: `str`, State to verify

        ### Returns
        - `bool`, True if it is correct, False if not

        ### Errors raised
        - None

        ### Function / Notes
        - This is spotipy2's built in state_verifier
        """
        return state == self.expected_state


class OauthServer(web.Application):
    def __init__(self, authenticated_html_response: str, failed_html_response: str, state_verifier: Callable):
        self.code = None  # The code is *not* the access token
        self.state = None

        self.authenticated_html_response = authenticated_html_response
        self.failed_html_response = failed_html_response
        self.state_verifier = state_verifier

        super().__init__()
        self.add_routes([web.get('/', self.authorized)])

    async def authorized(self, request):
        self.state = request.rel_url.query['state']

        if await self.state_verifier(self.state):
            self.code = request.rel_url.query['code']
            return web.FileResponse(self.authenticated_html_response)
        else:
            return web.FileResponse(self.failed_html_response)
