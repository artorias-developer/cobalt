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
from domain.enums import PermissionsEnum
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import AbstractAuthService
from application.dtos import UserDto


class HttpBaseRouter:
    """
    Base router.
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
            raise AuthenticationError(self._("Invalid session"))

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

        Raises:
        - AuthenticationError: If user is not authenticated.
        - PermissionsError: If user does not have required permissions.
        """
        async def dependency(request: Request) -> UserDto:
            user = getattr(request.state, "user", None)

            if not user:
                raise AuthenticationError(self._("Invalid session"))

            if not any(permission in user.role.permissions for permission in permissions):
                raise PermissionsError(self._("Not enough permissions"))

            return user

        return dependency