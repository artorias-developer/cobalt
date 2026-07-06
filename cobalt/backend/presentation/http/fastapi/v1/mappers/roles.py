#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.dtos import (
    RoleDto,
    RolesGetPageDto,
    RolesPageDto,
    RoleCreateDto,
    RoleUpdateDto
)
from presentation.contracts.http.mappers import AbstractRolesRouterMapper
from presentation.http.fastapi.v1.schemas import (
    RoleSchema,
    RolesGetPageSchema,
    RolesPageSchema,
    RoleCreateSchema,
    RoleUpdateSchema
)


class RolesRouterMapper(AbstractRolesRouterMapper):
    """
    Mapper for roles router.
    """

    def dto_to_schema(
        self,
        dto: RoleDto
    ) -> RoleSchema:
        """
        Converts RoleDto object to RoleSchema object.

        Parameters:
        - dto: RoleDto object.

        Returns:
        - RoleSchema: RoleSchema object.
        """
        return RoleSchema(
            id=dto.id,
            name=dto.name,
            permissions=dto.permissions,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    def dtos_to_schemas(
        self,
        dtos: List[RoleDto]
    ) -> List[RoleSchema]:
        """
        Converts RoleDto objects to RoleSchema objects.

        Parameters:
        - dtos: List of RoleDto objects.

        Returns:
        - List: List of RoleSchema objects.
        """
        return [
            self.dto_to_schema(dto)
            for dto in dtos
        ]

    def page_dto_to_schema(
        self,
        dto: RolesPageDto
    ) -> RolesPageSchema:
        """
        Converts RolesPageDto object to RolesPageSchema object.

        Parameters:
        - dto: RolesPageDto object.

        Returns:
        - RolesPageSchema: RolesPageSchema object.
        """
        return RolesPageSchema(
            roles=self.dtos_to_schemas(
                dtos=dto.roles
            ),
            total=dto.total,
            page=dto.page,
            pages=dto.pages
        )

    def get_page_schema_to_dto(
        self,
        schema: RolesGetPageSchema
    ) -> RolesGetPageDto:
        """
        Converts RolesGetPageSchema object to RolesGetPageDto object.

        Parameters:
        - schema: RolesGetPageSchema object.

        Returns:
        - RolesGetPageDto: RolesGetPageDto object.
        """
        return RolesGetPageDto(
            page=schema.page,
            search=schema.search,
            sort_field=schema.sort_field,
            sort_direction=schema.sort_direction,
            limit=schema.limit
        )

    def create_schema_to_dto(
        self,
        schema: RoleCreateSchema
    ) -> RoleCreateDto:
        """
        Converts RoleCreateSchema object to RoleCreateDto object.

        Parameters:
        - schema: RoleCreateSchema object.

        Returns:
        - RoleCreateDto: RoleCreateDto object.
        """
        return RoleCreateDto(
            name=schema.name,
            permissions=schema.permissions
        )

    def update_schema_to_dto(
        self,
        schema: RoleUpdateSchema
    ) -> RoleUpdateDto:
        """
        Converts RoleUpdateSchema object to RoleUpdateDto object.

        Parameters:
        - schema: RoleUpdateSchema object.

        Returns:
        - RoleUpdateDto: RoleUpdateDto object.
        """
        return RoleUpdateDto(
            name=schema.name,
            permissions=schema.permissions
        )
