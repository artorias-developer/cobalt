#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import List

from application.dtos import (
    AttributeDto,
    AttributesGetPageDto,
    AttributesPageDto,
    AttributeCreateDto,
    AttributeUpdateDto
)


class AbstractAttributesService(ABC):
    """
    Abstract attributes service.
    """

    @abstractmethod
    async def get_page(
        self,
        server_id: int,
        dto: AttributesGetPageDto
    ) -> AttributesPageDto:
        """
        Gets a paginated list of attributes.

        Parameters:
        - server_id: Server ID.
        - dto: AttributesGetPageDto object.

        Returns:
        - AttributesPageDto: AttributesPageDto object.
        """
        ...

    @abstractmethod
    async def get_one_by_id(
        self,
        server_id: int,
        attribute_id: int
    ) -> AttributeDto:
        """
        Gets an existing attribute by ID.

        Parameters:
        - server_id: Server ID.
        - attribute_id: Attribute ID.

        Returns:
        - AttributeDto: AttributeDto object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        server_id: int,
        dto: AttributeCreateDto
    ) -> AttributeDto:
        """
        Creates a new attribute.

        Parameters:
        - server_id: Server ID.
        - dto: AttributeCreateDto object.

        Returns:
        - AttributeDto: AttributeDto object.
        """
        ...

    @abstractmethod
    async def create_many(
        self,
        server_id: int,
        dtos: List[AttributeCreateDto]
    ) -> List[AttributeDto]:
        """
        Creates the new attributes.

        Parameters:
        - server_id: Server ID.
        - dtos: List of AttributeCreateDto objects.

        Returns:
        - List: List of AttributeDto objects.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        server_id: int,
        dto: AttributeUpdateDto
    ) -> AttributeDto:
        """
        Updates an existing attribute.

        Parameters:
        - server_id: Server ID.
        - dto: AttributeUpdateDto object.

        Returns:
        - AttributeDto: AttributeDto object.
        """
        ...

    @abstractmethod
    async def update_many(
        self,
        server_id: int,
        dtos: List[AttributeUpdateDto]
    ) -> List[AttributeDto]:
        """
        Updates an existing attributes.

        Parameters:
        - server_id: Server ID.
        - dtos: List of AttributeUpdateDto objects.

        Returns:
        - List: List of AttributeDto objects.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        server_id: int,
        attribute_id: int
    ) -> None:
        """
        Deletes an existing attributes.

        Parameters:
        - server_id: Server ID.
        - attribute_id: Attribute ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def delete_many(
        self,
        server_id: int,
        attribute_ids: List[int]
    ) -> None:
        """
        Deletes an existing attributes.

        Parameters:
        - server_id: Server ID.
        - attribute_ids: List of attribute IDs.

        Returns:
        - None.
        """
        ...