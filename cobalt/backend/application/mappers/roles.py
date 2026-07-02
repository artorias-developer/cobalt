#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import RoleName
from domain.entities import (
    RoleEntity,
    RolesPageEntity,
    RolesGetPageEntity,
    RoleCreateEntity,
    RoleUpdateEntity
)
from application.contracts.mappers import AbstractRolesServiceMapper
from application.dtos import (
    RoleDto,
    RolesPageDto,
    RolesGetPageDto,
    RoleCreateDto,
    RoleUpdateDto
)


class RolesServiceMapper(AbstractRolesServiceMapper):
    """
    Mapper for roles service.
    """

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
        return RoleDto(
            id=entity.id,
            name=entity.name.value,
            permissions=entity.permissions,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

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
        return [
            self.entity_to_dto(entity)
            for entity in entities
        ]

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
        return RolesPageDto(
            roles=self.entities_to_dtos(
                entities=entity.roles
            ),
            total=entity.total,
            page=entity.page,
            pages=entity.pages
        )

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
        return RolesGetPageEntity(
            page=dto.page,
            search=dto.search,
            sort_field=dto.sort_field,
            sort_direction=dto.sort_direction,
            limit=dto.limit
        )

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
        return RoleCreateEntity(
            name=RoleName(dto.name),
            permissions=dto.permissions
        )

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
        return RoleUpdateEntity(
            id=role_id,
            name=RoleName(dto.name) if dto.name is not None else None,
            permissions=dto.permissions
        )
