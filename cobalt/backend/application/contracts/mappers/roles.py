#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List

from domain.entities import (
    RoleEntity,
    RolesPageEntity,
    RolesGetPageEntity,
    RoleCreateEntity,
    RoleUpdateEntity
)
from application.dtos import (
    RoleDto,
    RolesPageDto,
    RolesGetPageDto,
    RoleCreateDto,
    RoleUpdateDto
)


class AbstractRolesServiceMapper(ABC):
    """
    Abstract mapper for roles service.
    """

    @abstractmethod
    def entity_to_dto(
        self,
        entity: RoleEntity
    ) -> RoleDto:
        """
        Converts RoleEntity object to RoleDto object.

        Parameters:
        - entity: RoleEntity object.

        Returns:
        - RoleDto: RoleDto object.
        """
        ...

    @abstractmethod
    def entities_to_dtos(
        self,
        entities: List[RoleEntity]
    ) -> List[RoleDto]:
        """
        Converts RoleEntity objects to RoleDto objects.

        Parameters:
        - entities: List of RoleEntity objects.

        Returns:
        - List: List of RoleDto objects.
        """
        ...

    @abstractmethod
    def page_entity_to_dto(
        self,
        entity: RolesPageEntity
    ) -> RolesPageDto:
        """
        Converts RolesPageEntity object to RolesPageDto object.

        Parameters:
        - entity: RolesPageEntity object.

        Returns:
        - RolesPageDto: RolesPageDto object.
        """
        ...

    @abstractmethod
    def get_page_dto_to_entity(
        self,
        dto: RolesGetPageDto
    ) -> RolesGetPageEntity:
        """
        Converts RolesGetPageDto object to RolesGetPageEntity object.

        Parameters:
        - dto: RolesGetPageDto object.

        Returns:
        - RolesGetPageEntity: RolesGetPageEntity object.
        """
        ...

    @abstractmethod
    def create_dto_to_entity(
        self,
        dto: RoleCreateDto
    ) -> RoleCreateEntity:
        """
        Converts RoleCreateDto object to RoleCreateEntity object.

        Parameters:
        - dto: RoleCreateDto object.

        Returns:
        - RoleCreateEntity: RoleCreateEntity object.
        """
        ...

    @abstractmethod
    def update_dto_to_entity(
        self,
        role_id: int,
        dto: RoleUpdateDto
    ) -> RoleUpdateEntity:
        """
        Converts RoleUpdateDto object to RoleUpdateEntity object.

        Parameters:
        - role_id: Role ID.
        - dto: RoleUpdateDto object.

        Returns:
        - RoleUpdateEntity: RoleUpdateEntity object.
        """
        ...
