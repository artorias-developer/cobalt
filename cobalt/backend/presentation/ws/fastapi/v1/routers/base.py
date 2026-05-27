#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Callable, List

from fastapi import WebSocket, WebSocketException

from domain.exceptions import (
    PermissionsError,
    AuthenticationError
)
from domain.enums import PermissionsEnum
from application.contracts.services import AbstractAuthService
from application.dtos import UserDto
from presentation.shared import CookieConstants
from presentation.ws.shared import WebSocketStatusCodesEnum


class BaseWsRouter:
    """
    Base WebSockets router.
    """
    auth_service: AbstractAuthService

    def __init__(
        self,
        auth_service: AbstractAuthService
    ):
        self.auth_service = auth_service

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
        """
        if hasattr(websocket.state, "user"):
            return websocket.state.user

        session_id = websocket.cookies.get(CookieConstants.SESSION_KEY)

        if not session_id:
            raise WebSocketException(
                code=WebSocketStatusCodesEnum.WS_4401_UNAUTHORIZED,
                reason="Not authenticated"
            )

        user = await self.auth_service.get_session_user(
            session_id=session_id
        )

        if not user:
            raise WebSocketException(
                code=WebSocketStatusCodesEnum.WS_4401_UNAUTHORIZED,
                reason="Invalid session"
            )

        websocket.state.user = user

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
        """
        async def dependency(websocket: WebSocket) -> UserDto:
            if not hasattr(websocket.state, "user"):
                raise AuthenticationError("Not authenticated")

            user = websocket.state.user

            if not any(permission in user.role.permissions for permission in permissions):
                raise PermissionsError("Not enough permissions")

            return user

        return dependency
