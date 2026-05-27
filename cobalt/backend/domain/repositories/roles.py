#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, List, Any

from domain.entities import (
    RoleEntity,
    RolesPageEntity,
    RolesGetPageEntity,
    RoleCreateEntity,
    RoleUpdateEntity
)


class AbstractRolesRepository(ABC):
    """
    Abstract roles repository.
    """

    @abstractmethod
    async def get_page(
        self,
        entity: RolesGetPageEntity,
        session: Optional[Any] = None
    ) -> RolesPageEntity:
        """
        Gets a paginated list of roles.

        Parameters:
        - entity: RolesGetPageEntity object.
        - session: Session object.

        Returns:
        - RolesPageEntity: RolesPageEntity object.
        """
        ...

    @abstractmethod
    async def get_one_by_id(
        self,
        role_id: int,
        session: Optional[Any] = None
    ) -> Optional[RoleEntity]:
        """
        Gets an existing role by ID.

        Parameters:
        - role_id: Role ID.
        - session: Session object.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        entity: RoleCreateEntity,
        session: Optional[Any] = None
    ) -> RoleEntity:
        """
        Creates a new role.

        Parameters:
        - entity: RoleCreateEntity object.
        - session: Session object.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        entity: RoleUpdateEntity,
        session: Optional[Any] = None
    ) -> Optional[RoleEntity]:
        """
        Updates an existing role.

        Parameters:
        - entity: RoleUpdateEntity object.
        - session: Session object.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        role_id: int,
        session: Optional[Any] = None
    ) -> Optional[RoleEntity]:
        """
        Deletes an existing role.

        Parameters:
        - role_id: Role ID.
        - session: Session object.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        ...

    @abstractmethod
    async def delete_many(
        self,
        role_ids: List[int],
        session: Optional[Any] = None
    ) -> List[RoleEntity]:
        """
        Deletes multiple existing roles.

        Parameters:
        - role_ids: List of role IDs.
        - session: Session object.

        Returns:
        - List: List of RoleEntity objects.
        """
        ...