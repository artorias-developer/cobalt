#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request

from domain.enums import LanguageEnum
from application.contracts.managers import AbstractI18nManager
from presentation.shared import CookieConstants


class HttpLocaleMiddleware:
    """
    Middleware for detecting language from user settings and activating gettext translations.
    """
    app: ASGIApp
    i18n_manager: AbstractI18nManager

    def __init__(
        self,
        app: ASGIApp,
        i18n_manager: AbstractI18nManager
    ):
        self.app = app
        self.i18n_manager = i18n_manager

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
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        language = self.i18n_manager.get_default_language()
        user = getattr(request.state, "user", None)

        if user:
            try:
                language = LanguageEnum(user.settings.language)
            except (ValueError, TypeError, AttributeError):
                pass
        else:
            cookie_language = request.cookies.get(CookieConstants.LANGUAGE_KEY)

            if cookie_language:
                try:
                    language = LanguageEnum(cookie_language)
                except ValueError:
                    pass

        self.i18n_manager.activate(language)
        scope["state"]["language"] = language

        await self.app(scope, receive, send)