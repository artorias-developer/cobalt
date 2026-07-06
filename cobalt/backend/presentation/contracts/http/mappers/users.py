#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any, List

from application.dtos import (
    UserDto,
    UsersGetPageDto,
    UsersPageDto,
    UserCreateDto,
    UserUpdateDto
)


class AbstractUsersRouterMapper(ABC):
    """
    Abstract mapper for users router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: UserDto
    ) -> Any:
        """
        Converts UserDto object to schema object.

        Parameters:
        - dto: UserDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def dto_to_me_schema(
        self,
        dto: UserDto
    ) -> Any:
        """
        Converts UserDto object to schema object.

        Parameters:
        - dto: UserDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def dtos_to_schemas(
        self,
        dtos: List[UserDto]
    ) -> List[Any]:
        """
        Converts UserDto objects to schema objects.

        Parameters:
        - dtos: List of UserDto objects.

        Returns:
        - List: List of any schema objects.
        """
        ...

    @abstractmethod
    def page_dto_to_schema(
        self,
        dto: UsersPageDto
    ) -> Any:
        """
        Converts UsersPageDto object to schema object.

        Parameters:
        - dto: UsersPageDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def get_page_schema_to_dto(
        self,
        schema: Any
    ) -> UsersGetPageDto:
        """
        Converts schema object to UsersGetPageDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - UsersGetPageDto: UsersGetPageDto object.
        """
        ...

    @abstractmethod
    def create_schema_to_dto(
        self,
        schema: Any
    ) -> UserCreateDto:
        """
        Converts schema object to UserCreateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - UserCreateDto: UserCreateDto object.
        """
        ...

    @abstractmethod
    def update_schema_to_dto(
        self,
        schema: Any
    ) -> UserUpdateDto:
        """
        Converts schema object to UserUpdateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - UserUpdateDto: UserUpdateDto object.
        """
        ...
