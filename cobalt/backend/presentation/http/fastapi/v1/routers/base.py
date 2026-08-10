#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Callable, List

from fastapi import Request

from domain.exceptions import (
    AuthenticationError,
    PermissionsError
)
from domain.enums import PermissionEnum
from application.contracts.services import AbstractAuthService
from application.dtos import UserDto


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

        Raises:
        - AuthenticationError: If user is not authenticated.
        """
        user = getattr(request.state, "user", None)

        if not user:
            raise AuthenticationError("Invalid session")

        return user

    def http_permission_required(
        self,
        permissions: List[PermissionEnum]
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
        async def dependency(request: Request) -> UserDto:
            user = getattr(request.state, "user", None)

            if not user:
                raise AuthenticationError("Invalid session")

            if not any(permission in user.role.permissions for permission in permissions):
                raise PermissionsError("Not enough permissions")

            return user

        return dependency