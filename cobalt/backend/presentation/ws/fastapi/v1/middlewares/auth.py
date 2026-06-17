#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.websockets import WebSocket

from application.contracts.services import AbstractAuthService
from presentation.shared import CookieConstants


class WsAuthMiddleware:
    """
    Middleware for authenticating user via session cookie for WebSocket connections.
    """
    _app: ASGIApp
    _auth_service: AbstractAuthService

    def __init__(
        self,
        app: ASGIApp,
        auth_service: AbstractAuthService
    ):
        self._app = app
        self._auth_service = auth_service

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:
        """
        Authenticates user via session cookie and stores it in websocket state.

        Parameters:
        - scope: ASGI scope.
        - receive: ASGI receive channel.
        - send: ASGI send channel.

        Returns:
        - None.
        """
        if scope["type"] == "websocket":
            websocket = WebSocket(scope, receive, send)
            session_id = websocket.cookies.get(CookieConstants.SESSION_KEY)

            if session_id:
                try:
                    user = await self._auth_service.get_session_user(
                        session_id=session_id
                    )

                    if user:
                        scope["state"]["user"] = user
                except Exception:
                    pass

        await self._app(scope, receive, send)
