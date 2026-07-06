#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.dtos import (
    AttributeDto,
    AttributesGetPageDto,
    AttributesPageDto,
    AttributeCreateDto,
    AttributeUpdateDto
)
from presentation.contracts.http.mappers import AbstractAttributesRouterMapper
from presentation.http.fastapi.v1.schemas import (
    AttributeSchema,
    AttributesGetPageSchema,
    AttributesPageSchema,
    AttributeCreateSchema,
    AttributeUpdateSchema,
    AttributesUpdateSchema
)


class AttributesRouterMapper(AbstractAttributesRouterMapper):
    """
    Mapper for attributes router.
    """

    def dto_to_schema(
        self,
        dto: AttributeDto
    ) -> AttributeSchema:
        """
        Converts AttributeDto object to AttributeSchema object.

        Parameters:
        - dto: AttributeDto object.

        Returns:
        - AttributeSchema: AttributeSchema object.
        """
        return AttributeSchema(
            id=dto.id,
            server_id=dto.server_id,
            key=dto.key,
            value=dto.value,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    def dtos_to_schemas(
        self,
        dtos: List[AttributeDto]
    ) -> List[AttributeSchema]:
        """
        Converts AttributeDto objects to AttributeSchema objects.

        Parameters:
        - dtos: List of AttributeDto objects.

        Returns:
        - List: List of AttributeSchema objects.
        """
        return [
            self.dto_to_schema(dto)
            for dto in dtos
        ]

    def page_dto_to_schema(
        self,
        dto: AttributesPageDto
    ) -> AttributesPageSchema:
        """
        Converts AttributesPageDto object to AttributesPageSchema object.

        Parameters:
        - dto: AttributesPageDto object.

        Returns:
        - AttributesPageSchema: AttributesPageSchema object.
        """
        return AttributesPageSchema(
            attributes=self.dtos_to_schemas(
                dtos=dto.attributes
            ),
            total=dto.total,
            page=dto.page,
            pages=dto.pages
        )

    def get_page_schema_to_dto(
        self,
        schema: AttributesGetPageSchema
    ) -> AttributesGetPageDto:
        """
        Converts AttributesGetPageSchema object to AttributesGetPageDto object.

        Parameters:
        - schema: AttributesGetPageSchema object.

        Returns:
        - AttributesGetPageDto: AttributesGetPageDto object.
        """
        return AttributesGetPageDto(
            page=schema.page,
            search=schema.search,
            sort_field=schema.sort_field,
            sort_direction=schema.sort_direction,
            limit=schema.limit
        )

    def create_schema_to_dto(
        self,
        schema: AttributeCreateSchema
    ) -> AttributeCreateDto:
        """
        Converts AttributeCreateSchema object to AttributeCreateDto object.

        Parameters:
        - schema: AttributeCreateSchema object.

        Returns:
        - AttributeCreateDto: AttributeCreateDto object.
        """
        return AttributeCreateDto(
            key=schema.key,
            value=schema.value
        )

    def create_schemas_to_dtos(
        self,
        schemas: List[AttributeCreateSchema]
    ) -> List[AttributeCreateDto]:
        """
        Converts AttributeCreateSchema objects to AttributeCreateDto objects.

        Parameters:
        - schemas: List of AttributeCreateSchema objects.

        Returns:
        - List: List of AttributeCreateDto objects.
        """
        return [
            self.create_schema_to_dto(schema)
            for schema in schemas
        ]

    def update_schema_to_dto(
        self,
        attribute_id: int,
        schema: AttributeUpdateSchema
    ) -> AttributeUpdateDto:
        """
        Converts AttributeUpdateSchema object to AttributeUpdateDto object.

        Parameters:
        - attribute_id: Attribute ID.
        - schema: AttributeUpdateSchema object.

        Returns:
        - AttributeUpdateDto: AttributeUpdateDto object.
        """
        return AttributeUpdateDto(
            id=attribute_id,
            key=schema.key,
            value=schema.value
        )

    def update_schemas_to_dtos(
        self,
        schemas: List[AttributesUpdateSchema]
    ) -> List[AttributeUpdateDto]:
        """
        Converts AttributesUpdateSchema objects to AttributeUpdateDto objects.

        Parameters:
        - schemas: List of AttributesUpdateSchema objects.

        Returns:
        - List: List of AttributeUpdateDto objects.
        """
        return [
            AttributeUpdateDto(
                id=schema.id,
                key=schema.key,
                value=schema.value
            )
            for schema in schemas
        ]
