#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from starlette.types import ASGIApp, Receive, Scope, Send

from domain.enums import LanguageEnum
from application.contracts.managers import AbstractI18nManager


class WsLocaleMiddleware:
    """
    Middleware for detecting language from user settings and activating gettext translations for WebSocket connections.
    """
    _app: ASGIApp
    _i18n_manager: AbstractI18nManager

    def __init__(
        self,
        app: ASGIApp,
        i18n_manager: AbstractI18nManager
    ):
        self._app = app
        self._i18n_manager = i18n_manager

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:
        """
        Detects language from user settings and activates translations.

        Parameters:
        - scope: ASGI scope.
        - receive: ASGI receive channel.
        - send: ASGI send channel.

        Returns:
        - None.
        """
        if scope["type"] != "websocket":
            await self._app(scope, receive, send)
            return

        language = self._i18n_manager.get_default_language()
        user = scope.get("state", {}).get("user")

        if user:
            try:
                language = LanguageEnum(user.settings.language)
            except (ValueError, TypeError, AttributeError):
                pass

        self._i18n_manager.activate(language)
        scope["state"]["language"] = language

        await self._app(scope, receive, send)