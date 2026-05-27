#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, List, Any

from domain.entities import (
    UserEntity,
    UsersPageEntity,
    UsersGetPageEntity,
    UserCreateEntity,
    UserUpdateEntity
)


class AbstractUsersRepository(ABC):
    """
    Abstract users repository.
    """

    @abstractmethod
    async def get_page(
        self,
        entity: UsersGetPageEntity,
        session: Optional[Any] = None
    ) -> UsersPageEntity:
        """
        Gets a paginated list of users.

        Parameters:
        - entity: UsersGetPageEntity object.
        - session: Session object.

        Returns:
        - UsersPageEntity: UsersPageEntity object.
        """
        ...

    @abstractmethod
    async def get_one_by_id(
        self,
        user_id: int,
        session: Optional[Any] = None
    ) -> Optional[UserEntity]:
        """
        Gets an existing user by ID.

        Parameters:
        - user_id: User ID.
        - session: Session object.

        Returns:
        - UserEntity: UserEntity object.
        """
        ...

    @abstractmethod
    async def get_one_by_login(
        self,
        login: str,
        session: Optional[Any] = None
    ) -> Optional[UserEntity]:
        """
        Gets an existing user by login.

        Parameters:
        - login: Login of the user.
        - session: Session object.

        Returns:
        - UserEntity: UserEntity object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        entity: UserCreateEntity,
        session: Optional[Any] = None
    ) -> UserEntity:
        """
        Creates a new user.

        Parameters:
        - entity: UserCreateEntity object.
        - session: Session object.

        Returns:
        - UserEntity: UserEntity object.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        entity: UserUpdateEntity,
        session: Optional[Any] = None
    ) -> Optional[UserEntity]:
        """
        Updates an existing user.

        Parameters:
        - entity: UserUpdateEntity object.
        - session: Session object.

        Returns:
        - UserEntity: UserEntity object.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        user_id: int,
        session: Optional[Any] = None
    ) -> Optional[UserEntity]:
        """
        Deletes an existing user.

        Parameters:
        - user_id: User ID.
        - session: Session object.

        Returns:
        - UserEntity: UserEntity object.
        """
        ...

    @abstractmethod
    async def delete_many(
        self,
        user_ids: List[int],
        session: Optional[Any] = None
    ) -> List[UserEntity]:
        """
        Deletes multiple existing users.

        Parameters:
        - user_ids: List of user IDs.
        - session: Session object.

        Returns:
        - List: List of UserEntity objects.
        """
        ...