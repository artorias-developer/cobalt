#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import List

from application.dtos import (
    RoleDto,
    RolesGetPageDto,
    RolesPageDto,
    RoleCreateDto,
    RoleUpdateDto
)


class AbstractRolesService(ABC):
    """
    Abstract roles service.
    """

    @abstractmethod
    async def get_page(
        self,
        dto: RolesGetPageDto
    ) -> RolesPageDto:
        """
        Gets a paginated list of roles.

        Parameters:
        - dto: RolesGetPageDto object.

        Returns:
        - RolesPageDto: RolesPageDto object.
        """
        ...

    @abstractmethod
    async def get_one_by_id(
        self,
        role_id: int
    ) -> RoleDto:
        """
        Gets an existing role by ID.

        Parameters:
        - role_id: Role ID.

        Returns:
        - RoleDto: RoleDto object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        dto: RoleCreateDto
    ) -> RoleDto:
        """
        Creates a new role.

        Parameters:
        - dto: RoleCreateDto object.

        Returns:
        - RoleDto: RoleDto object.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        role_id: int,
        dto: RoleUpdateDto
    ) -> RoleDto:
        """
        Updates an existing role.

        Parameters:
        - role_id: Role ID.
        - dto: RoleUpdateDto object.

        Returns:
        - RoleDto: RoleDto object.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        role_id: int
    ) -> None:
        """
        Deletes an existing role.

        Parameters:
        - role_id: Role ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def delete_many(
        self,
        role_ids: List[int]
    ) -> None:
        """
        Deletes multiple existing roles.

        Parameters:
        - role_ids: List of role IDs.

        Returns:
        - None.
        """
        ...