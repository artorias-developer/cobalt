#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Callable, List

from fastapi import WebSocket, WebSocketException

from domain.exceptions import (
    PermissionsError,
    AuthenticationError
)
from domain.enums import PermissionsEnum
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import AbstractAuthService
from application.dtos import UserDto
from presentation.ws.shared import WebSocketStatusCodesEnum


class BaseWsRouter:
    """
    Base WebSockets router.
    """
    auth_service: AbstractAuthService
    i18n_manager: AbstractI18nManager

    _: Callable

    def __init__(
        self,
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        self.auth_service = auth_service
        self.i18n_manager = i18n_manager

        self._ = i18n_manager.gettext

    async def ws_session_required(
        self,
        websocket: WebSocket
    ) -> UserDto:
        """
        Checks if user is authenticated.

        Parameters:
        - websocket: WebSockets object.

        Returns:
        - UserDto: UserDto object.

        Raises:
        - WebSocketException: If user is not authenticated.
        """
        user = getattr(websocket.state, "user", None)

        if not user:
            raise WebSocketException(
                code=WebSocketStatusCodesEnum.WS_4401_UNAUTHORIZED,
                reason=self._("Invalid session")
            )

        return user

    def ws_permission_required(
        self,
        permissions: List[PermissionsEnum]
    ) -> Callable:
        """
        Checks if user has at least one of the required permissions.

        Parameters:
        - permissions: List of PermissionsEnum values representing the required permissions.

        Returns:
        - Callable: Dependency function.

        Raises:
        - AuthenticationError: If user is not authenticated.
        - PermissionsError: If user does not have required permissions.
        """
        async def dependency(websocket: WebSocket) -> UserDto:
            user = getattr(websocket.state, "user", None)

            if not user:
                raise AuthenticationError(self._("Invalid session"))

            if not any(permission in user.role.permissions for permission in permissions):
                raise PermissionsError(self._("Not enough permissions"))

            return user

        return dependency