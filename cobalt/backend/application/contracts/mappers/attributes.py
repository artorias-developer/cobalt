#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List

from domain.entities import (
    AttributeEntity,
    AttributesPageEntity,
    AttributesGetPageEntity,
    AttributeCreateEntity,
    AttributeUpdateEntity
)
from application.dtos import (
    AttributeDto,
    AttributesPageDto,
    AttributesGetPageDto,
    AttributeCreateDto,
    AttributeUpdateDto
)


class AbstractAttributesServiceMapper(ABC):
    """
    Abstract mapper for attributes service.
    """

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...
