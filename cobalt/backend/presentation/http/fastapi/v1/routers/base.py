#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Callable, List

from fastapi import Request

from domain.exceptions import (
    AuthenticationError,
    PermissionsError
)
from domain.enums import PermissionsEnum
from application.contracts.services import AbstractAuthService
from application.dtos import UserDto
from presentation.shared import CookieConstants


class HttpBaseRouter:
    """
    Base router.
    """
    auth_service: AbstractAuthService

    def __init__(
        self,
        auth_service: AbstractAuthService
    ):
        self.auth_service = auth_service

    async def http_session_required(
        self,
        request: Request
    ) -> UserDto:
        """
        Checks if user is authenticated.

        Parameters:
        - request: Request object.

        Returns:
        - UserDto: UserDto object.
        """
        if hasattr(request.state, "user"):
            return request.state.user

        session_id = request.cookies.get(CookieConstants.SESSION_KEY)

        if not session_id:
            raise AuthenticationError("Not authenticated")

        user = await self.auth_service.get_session_user(
            session_id=session_id
        )

        if not user:
            raise AuthenticationError("Invalid session")

        request.state.user = user

        return user

    def http_permission_required(
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
        async def dependency(request: Request) -> UserDto:
            if not hasattr(request.state, "user"):
                raise AuthenticationError("Not authenticated")

            user = request.state.user

            if not any(permission in user.role.permissions for permission in permissions):
                raise PermissionsError("Not enough permissions")

            return user

        return dependency
