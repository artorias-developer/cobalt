#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, List

from domain.entities import (
    UserEntity,
    UsersPageEntity,
    UsersGetPageEntity,
    UserCreateEntity,
    UserUpdateEntity
)
from application.dtos import (
    UserDto,
    UsersPageDto,
    UsersGetPageDto,
    UserCreateDto,
    UserUpdateDto
)


class AbstractUsersServiceMapper(ABC):
    """
    Abstract mapper for users service.
    """

    @abstractmethod
    def entity_to_dto(
        self,
        entity: UserEntity
    ) -> UserDto:
        """
        Converts UserEntity object to UserDto object.

        Parameters:
        - entity: UserEntity object.

        Returns:
        - UserDto: UserDto object.
        """
        ...

    @abstractmethod
    def entities_to_dtos(
        self,
        entities: List[UserEntity]
    ) -> List[UserDto]:
        """
        Converts UserEntity objects to UserDto objects.

        Parameters:
        - entities: List of UserEntity objects.

        Returns:
        - List: List of UserDto objects.
        """
        ...

    @abstractmethod
    def page_entity_to_dto(
        self,
        entity: UsersPageEntity
    ) -> UsersPageDto:
        """
        Converts UsersPageEntity object to UsersPageDto object.

        Parameters:
        - entity: UsersPageEntity object.

        Returns:
        - UsersPageDto: UsersPageDto object.
        """
        ...

    @abstractmethod
    def get_page_dto_to_entity(
        self,
        dto: UsersGetPageDto
    ) -> UsersGetPageEntity:
        """
        Converts UsersGetPageDto object to UsersGetPageEntity object.

        Parameters:
        - dto: UsersGetPageDto object.

        Returns:
        - UsersGetPageEntity: UsersGetPageEntity object.
        """
        ...

    @abstractmethod
    def create_dto_to_entity(
        self,
        dto: UserCreateDto,
        hashed_password: str,
        salt: str
    ) -> UserCreateEntity:
        """
        Converts UserCreateDto object to UserCreateEntity object.

        Parameters:
        - dto: UserCreateDto object.
        - hashed_password: Hashed password.
        - salt: User salt.

        Returns:
        - UserCreateEntity: UserCreateEntity object.
        """
        ...

    @abstractmethod
    def update_dto_to_entity(
        self,
        user_id: int,
        dto: UserUpdateDto,
        hashed_password: Optional[str] = None,
        salt: Optional[str] = None
    ) -> UserUpdateEntity:
        """
        Converts UserUpdateDto object to UserUpdateEntity object.

        Parameters:
        - user_id: User ID.
        - dto: UserUpdateDto object.
        - hashed_password: Hashed password.
        - salt: Password hashing salt.

        Returns:
        - UserUpdateEntity: UserUpdateEntity object.
        """
        ...
