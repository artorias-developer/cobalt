#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from application.dtos import (
    AttributeDto,
    AttributesGetPageDto,
    AttributesPageDto,
    AttributeCreateDto,
    AttributeUpdateDto
)


class AbstractAttributesRouterMapper(ABC):
    """
    Abstract mapper for attributes router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: AttributeDto
    ) -> Any:
        """
        Converts AttributeDto object to schema object.

        Parameters:
        - dto: AttributeDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def dtos_to_schemas(
        self,
        dtos: List[AttributeDto]
    ) -> List[Any]:
        """
        Converts AttributeDto objects to schema objects.

        Parameters:
        - dtos: List of AttributeDto objects.

        Returns:
        - List: List of any schema objects.
        """
        ...

    @abstractmethod
    def page_dto_to_schema(
        self,
        dto: AttributesPageDto
    ) -> Any:
        """
        Converts AttributesPageDto object to schema object.

        Parameters:
        - dto: AttributesPageDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def get_page_schema_to_dto(
        self,
        schema: Any
    ) -> AttributesGetPageDto:
        """
        Converts schema object to AttributesGetPageDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - AttributesGetPageDto: AttributesGetPageDto object.
        """
        ...

    @abstractmethod
    def create_schema_to_dto(
        self,
        schema: Any
    ) -> AttributeCreateDto:
        """
        Converts schema object to AttributeCreateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - AttributeCreateDto: AttributeCreateDto object.
        """
        ...

    @abstractmethod
    def create_schemas_to_dtos(
        self,
        schemas: List[Any]
    ) -> List[AttributeCreateDto]:
        """
        Converts schema objects to AttributeCreateDto objects.

        Parameters:
        - schemas: Schema objects.

        Returns:
        - List: List of AttributeCreateDto objects.
        """
        ...

    @abstractmethod
    def update_schema_to_dto(
        self,
        attribute_id: int,
        schema: Any
    ) -> AttributeUpdateDto:
        """
        Converts schema object to AttributeUpdateDto object.

        Parameters:
        - attribute_id: Attribute ID.
        - schema: Schema object.

        Returns:
        - AttributeUpdateDto: AttributeUpdateDto object.
        """
        ...

    @abstractmethod
    def update_schemas_to_dtos(
        self,
        schemas: List[Any]
    ) -> List[AttributeUpdateDto]:
        """
        Converts schema objects to AttributeUpdateDto objects.

        Parameters:
        - schemas: Schema objects.

        Returns:
        - List: List of AttributeUpdateDto objects.
        """
        ...
