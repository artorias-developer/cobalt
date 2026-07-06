#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from application.dtos import (
    RoleDto,
    RolesGetPageDto,
    RolesPageDto,
    RoleCreateDto,
    RoleUpdateDto
)


class AbstractRolesRouterMapper(ABC):
    """
    Abstract mapper for roles router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: RoleDto
    ) -> Any:
        """
        Converts RoleDto object to schema object.

        Parameters:
        - dto: RoleDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def dtos_to_schemas(
        self,
        dtos: List[RoleDto]
    ) -> List[Any]:
        """
        Converts RoleDto objects to schema objects.

        Parameters:
        - dtos: List of RoleDto objects.

        Returns:
        - List: List of any schema objects.
        """
        ...

    @abstractmethod
    def page_dto_to_schema(
        self,
        dto: RolesPageDto
    ) -> Any:
        """
        Converts RolesPageDto object to schema object.

        Parameters:
        - dto: RolesPageDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def get_page_schema_to_dto(
        self,
        schema: Any
    ) -> RolesGetPageDto:
        """
        Converts schema object to RolesGetPageDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - RolesGetPageDto: RolesGetPageDto object.
        """
        ...

    @abstractmethod
    def create_schema_to_dto(
        self,
        schema: Any
    ) -> RoleCreateDto:
        """
        Converts schema object to RoleCreateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - RoleCreateDto: RoleCreateDto object.
        """
        ...

    @abstractmethod
    def update_schema_to_dto(
        self,
        schema: Any
    ) -> RoleUpdateDto:
        """
        Converts schema object to RoleUpdateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - RoleUpdateDto: RoleUpdateDto object.
        """
        ...
