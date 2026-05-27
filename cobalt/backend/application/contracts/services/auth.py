#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional

from application.dtos import (
    UserDto,
    AuthLoginDto,
    AuthSessionDto,
    AuthChangeCredentialsDto
)


class AbstractAuthService(ABC):
    """
    Abstract auth service.
    """

    @abstractmethod
    async def login(
        self,
        dto: AuthLoginDto,
        old_session_id: Optional[str] = None
    ) -> AuthSessionDto:
        """
        Authenticates user and creates session.

        Parameters:
        - dto: AuthLoginDto object.
        - old_session_id: Old session ID.

        Returns:
        - AuthSessionDto: AuthSessionDto object.
        """
        ...

    @abstractmethod
    async def logout(
        self,
        session_id: str
    ) -> None:
        """
        Deletes user session.

        Parameters:
        - session_id: Session ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def change_credentials(
        self,
        user_id: int,
        dto: AuthChangeCredentialsDto
    ) -> None:
        """
        Changes user login and/or password.

        Parameters:
        - user_id: User ID.
        - dto: AuthChangeCredentialsDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def get_session_user(
        self,
        session_id: str
    ) -> Optional[UserDto]:
        """
        Gets session by ID.

        Parameters:
        - session_id: Session ID.

        Returns:
        - UserDto: UserDto object.
        """
        ...
