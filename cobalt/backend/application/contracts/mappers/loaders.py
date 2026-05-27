#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List

from domain.entities import (
    LoaderEntity,
    LoaderCreateEntity,
    LoaderUpdateEntity
)
from application.dtos import (
    LoaderDto,
    LoaderCreateDto,
    LoaderUpdateDto,
)


class AbstractLoadersServiceMapper(ABC):
    """
    Abstract mapper for loaders service.
    """

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def update_dto_to_entity(
        self,
        dto: LoaderUpdateDto
    ) -> LoaderUpdateEntity:
        """
        Converts LoaderUpdateDto object to LoaderUpdateEntity object.

        Parameters:
        - dto: LoaderUpdateDto object.

        Returns:
        - LoaderUpdateEntity: LoaderUpdateEntity object.
        """
        ...
