#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import LoaderName
from domain.entities import (
    LoaderEntity,
    LoaderCreateEntity,
    LoaderUpdateEntity
)
from application.contracts.mappers import AbstractLoadersServiceMapper
from application.dtos import (
    LoaderDto,
    LoaderCreateDto,
    LoaderUpdateDto
)


class LoadersServiceMapper(AbstractLoadersServiceMapper):
    """
    Mapper for loaders service.
    """

    def entity_to_dto(
        self,
        entity: LoaderEntity
    ) -> LoaderDto:
        """
        Converts LoaderEntity object to LoaderDto object.

        Parameters:
        - entity: LoaderEntity object.

        Returns:
        - LoaderDto: LoaderDto object.
        """
        return LoaderDto(
            id=entity.id,
            game_id=entity.game_id,
            name=entity.name.value,
            versions=entity.versions,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def entities_to_dtos(
        self,
        entities: List[LoaderEntity]
    ) -> List[LoaderDto]:
        """
        Converts LoaderEntity objects to LoaderDto objects.

        Parameters:
        - entities: List of LoaderEntity objects.

        Returns:
        - List: List of LoaderDto objects.
        """
        return [
            self.entity_to_dto(entity)
            for entity in entities
        ]

    def create_dto_to_entity(
        self,
        dto: LoaderCreateDto
    ) -> LoaderCreateEntity:
        """
        Converts LoaderCreateDto object to LoaderCreateEntity object.

        Parameters:
        - dto: LoaderCreateDto object.

        Returns:
        - LoaderCreateEntity: LoaderCreateEntity object.
        """
        return LoaderCreateEntity(
            name=LoaderName(dto.name),
            versions=dto.versions
        )

    def update_dto_to_entity(
        self,
        dto: LoaderUpdateDto
    ) -> LoaderUpdateEntity:
        """
        Converts LoaderUpdateDto object to LoaderUpdateEntity object.

        Parameters:
        - loader_id: Loader ID.
        - dto: LoaderUpdateDto object.

        Returns:
        - LoaderUpdateEntity: LoaderUpdateEntity object.
        """
        return LoaderUpdateEntity(
            id=dto.id,
            name=LoaderName(dto.name) if dto.name is not None else None,
            versions=dto.versions
        )
