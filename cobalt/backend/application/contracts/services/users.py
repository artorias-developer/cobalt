#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import List

from application.dtos import (
    UserDto,
    UsersGetPageDto,
    UsersPageDto,
    UserCreateDto,
    UserUpdateDto
)


class AbstractUsersService(ABC):
    """
    Abstract users service.
    """

    @abstractmethod
    async def get_page(
        self,
        dto: UsersGetPageDto
    ) -> UsersPageDto:
        """
        Gets a paginated list of users.

        Parameters:
        - dto: UsersGetPageDto object.

        Returns:
        - UsersPageDto: UsersPageDto object.
        """
        ...

    @abstractmethod
    async def get_one_by_id(
        self,
        user_id: int
    ) -> UserDto:
        """
        Gets an existing user by ID.

        Parameters:
        - user_id: User ID.

        Returns:
        - UserDto: UserDto object.
        """
        ...

    @abstractmethod
    async def get_one_by_login(
        self,
        login: str
    ) -> UserDto:
        """
        Gets an existing user by login.

        Parameters:
        - login: User login.

        Returns:
        - UserDto: UserDto object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        dto: UserCreateDto
    ) -> UserDto:
        """
        Creates a new user.

        Parameters:
        - dto: UserCreateDto object.

        Returns:
        - UserDto: UserDto object.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        user_id: int,
        dto: UserUpdateDto
    ) -> UserDto:
        """
        Updates an existing user.

        Parameters:
        - user_id: User ID.
        - dto: UserUpdateDto object.

        Returns:
        - UserDto: UserDto object.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        user_id: int
    ) -> None:
        """
        Deletes an existing user.

        Parameters:
        - user_id: User ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def delete_many(
        self,
        user_ids: List[int]
    ) -> None:
        """
        Deletes multiple existing users.

        Parameters:
        - user_ids: List of user IDs.

        Returns:
        - None.
        """
        ...