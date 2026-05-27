#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, List, Any

from domain.entities import (
    AttributeEntity,
    AttributesPageEntity,
    AttributesGetPageEntity,
    AttributeCreateEntity,
    AttributeUpdateEntity
)


class AbstractAttributesRepository(ABC):
    """
    Abstract attributes repository.
    """

    @abstractmethod
    async def get_page(
        self,
        server_id: int,
        entity: AttributesGetPageEntity,
        session: Optional[Any] = None
    ) -> AttributesPageEntity:
        """
        Gets a paginated list of attributes.

        Parameters:
        - server_id: Server ID.
        - entity: AttributesGetPageEntity object.
        - session: Session object.

        Returns:
        - AttributesPageEntity: AttributesPageEntity object.
        """
        ...

    @abstractmethod
    async def get_one_by_id(
        self,
        attribute_id: int,
        server_id: int,
        session: Optional[Any] = None
    ) -> Optional[AttributeEntity]:
        """
        Gets an existing attribute by ID.

        Parameters:
        - attribute_id: Attribute ID.
        - server_id: Server Attribute ID.
        - session: Session object.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        server_id: int,
        entity: AttributeCreateEntity,
        session: Optional[Any] = None
    ) -> AttributeEntity:
        """
        Creates the new attributes.

        Parameters:
        - server_id: Server ID.
        - entity: AttributeCreateEntity object.
        - session: Session object.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        ...

    @abstractmethod
    async def create_many(
        self,
        server_id: int,
        entities: List[AttributeCreateEntity],
        session: Optional[Any] = None
    ) -> List[AttributeEntity]:
        """
        Creates the new attributes.

        Parameters:
        - server_id: Server ID.
        - entities: List of AttributeCreateEntity objects.
        - session: Session object.

        Returns:
        - List: List of AttributeEntity objects.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        server_id: int,
        entity: AttributeUpdateEntity,
        session: Optional[Any] = None
    ) -> Optional[AttributeEntity]:
        """
        Updates an existing entity.

        Parameters:
        - server_id: Server ID.
        - entity: AttributeUpdateEntity object.
        - session: Session object.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        ...

    @abstractmethod
    async def update_many(
        self,
        server_id: int,
        entities: List[AttributeUpdateEntity],
        session: Optional[Any] = None
    ) -> List[AttributeEntity]:
        """
        Updates an existing attributes.

        Parameters:
        - server_id: Server ID.
        - entities: List of AttributeUpdateEntity objects.
        - session: Session object.

        Returns:
        - List: List of AttributeEntity objects.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        server_id: int,
        attribute_id: int,
        session: Optional[Any] = None
    ) -> Optional[AttributeEntity]:
        """
        Deletes an existing attributes.

        Parameters:
        - server_id: Server ID.
        - attribute_id: Attribute ID.
        - session: Session object.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        ...

    @abstractmethod
    async def delete_many(
        self,
        server_id: int,
        attribute_ids: List[int],
        session: Optional[Any] = None
    ) -> List[AttributeEntity]:
        """
        Deletes an existing attributes.

        Parameters:
        - server_id: Server ID.
        - attribute_ids: List of attribute IDs.
        - session: Session object.

        Returns:
        - List: List of AttributeEntity objects.
        """
        ...