#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import AttributeKey
from domain.entities import (
    AttributeEntity,
    AttributesPageEntity,
    AttributesGetPageEntity,
    AttributeCreateEntity,
    AttributeUpdateEntity
)
from application.contracts.mappers import AbstractAttributesServiceMapper
from application.dtos import (
    AttributeDto,
    AttributesPageDto,
    AttributesGetPageDto,
    AttributeCreateDto,
    AttributeUpdateDto
)


class AttributesServiceMapper(AbstractAttributesServiceMapper):
    """
    Mapper for attributes service.
    """

    def entity_to_dto(
        self,
        entity: AttributeEntity
    ) -> AttributeDto:
        """
        Converts AttributeEntity object to AttributeDto object.

        Parameters:
        - entity: AttributeEntity object.

        Returns:
        - AttributeDto: AttributeDto object.
        """
        return AttributeDto(
            id=entity.id,
            server_id=entity.server_id,
            key=entity.key.value,
            value=entity.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def entities_to_dtos(
        self,
        entities: List[AttributeEntity]
    ) -> List[AttributeDto]:
        """
        Converts AttributeEntity objects to AttributeDto objects.

        Parameters:
        - entities: List of AttributeEntity objects.

        Returns:
        - List: List of AttributeDto objects.
        """
        return [
            self.entity_to_dto(entity)
            for entity in entities
        ]

    def page_entity_to_dto(
        self,
        entity: AttributesPageEntity
    ) -> AttributesPageDto:
        """
        Converts AttributesPageEntity object to AttributesPageDto object.

        Parameters:
        - entity: AttributesPageEntity object.

        Returns:
        - AttributesPageDto: AttributesPageDto object.
        """
        return AttributesPageDto(
            attributes=self.entities_to_dtos(
                entities=entity.attributes
            ),
            total=entity.total,
            page=entity.page,
            pages=entity.pages
        )

    def get_page_dto_to_entity(
        self,
        dto: AttributesGetPageDto
    ) -> AttributesGetPageEntity:
        """
        Converts AttributesGetPageDto object to AttributesGetPageEntity object.

        Parameters:
        - dto: AttributesGetPageDto object.

        Returns:
        - AttributesGetPageEntity: AttributesGetPageEntity object.
        """
        return AttributesGetPageEntity(
            page=dto.page,
            search=dto.search,
            sort_field=dto.sort_field,
            sort_direction=dto.sort_direction,
            limit=dto.limit
        )

    def create_dto_to_entity(
        self,
        dto: AttributeCreateDto
    ) -> AttributeCreateEntity:
        """
        Converts AttributeCreateDto object to AttributeCreateEntity object.

        Parameters:
        - dto: AttributeCreateDto object.

        Returns:
        - AttributeCreateEntity: AttributeCreateEntity object.
        """
        return AttributeCreateEntity(
            key=AttributeKey(dto.key),
            value=dto.value
        )

    def create_dtos_to_entities(
        self,
        dtos: List[AttributeCreateDto]
    ) -> List[AttributeCreateEntity]:
        """
        Converts AttributeCreateDto objects to AttributeCreateEntity objects.

        Parameters:
        - dtos: List of AttributeCreateDto objects.

        Returns:
        - List: List of AttributeCreateEntity objects.
        """
        return [
            self.create_dto_to_entity(dto)
            for dto in dtos
        ]

    def update_dto_to_entity(
        self,
        dto: AttributeUpdateDto
    ) -> AttributeUpdateEntity:
        """
        Converts AttributeUpdateDto object to AttributeUpdateEntity object.

        Parameters:
        - dto: AttributeUpdateDto object.

        Returns:
        - AttributeUpdateEntity: AttributeUpdateEntity object.
        """
        return AttributeUpdateEntity(
            id=dto.id,
            key=AttributeKey(dto.key) if dto.key is not None else None,
            value=dto.value
        )

    def update_dtos_to_entities(
        self,
        dtos: List[AttributeUpdateDto]
    ) -> List[AttributeUpdateEntity]:
        """
        Converts AttributeUpdateDto objects to AttributeUpdateEntity objects.

        Parameters:
        - dtos: List of AttributeUpdateDto objects.

        Returns:
        - List: List of AttributeUpdateEntity objects.
        """
        return [
            self.update_dto_to_entity(dto)
            for dto in dtos
        ]
