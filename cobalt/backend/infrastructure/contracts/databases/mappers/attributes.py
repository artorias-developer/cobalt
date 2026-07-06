#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from domain.entities import (
    AttributeEntity,
    AttributeCreateEntity,
    AttributeUpdateEntity
)


class AbstractAttributesRepositoryMapper(ABC):
    """
    Abstract attributes repository mapper.
    """

    @abstractmethod
    def model_to_entity(
        self,
        model: Any
    ) -> AttributeEntity:
        """
        Converts ORM model to AttributeEntity object.

        Parameters:
        - model: ORM model.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        ...

    @abstractmethod
    def models_to_entities(
        self,
        models: List[Any]
    ) -> List[AttributeEntity]:
        """
        Converts ORM models to AttributeEntity objects.

        Parameters:
        - models: List of ORM models.

        Returns:
        - List: List of AttributeEntity objects.
        """
        ...

    @abstractmethod
    def create_entity_to_model(
        self,
        server_id: int,
        entity: AttributeCreateEntity
    ) -> Any:
        """
        Converts AttributeCreateEntity object to ORM model.

        Parameters:
        - server_id: Server ID.
        - entity: AttributeCreateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...

    @abstractmethod
    def create_entities_to_models(
        self,
        server_id: int,
        entities: List[AttributeCreateEntity]
    ) -> List[Any]:
        """
        Converts AttributeCreateEntity objects to ORM models.

        Parameters:
        - server_id: Server ID.
        - entities: List of AttributeCreateEntity objects.

        Returns:
        - List: List of ORM models.
        """
        ...

    @abstractmethod
    def update_entity_to_model(
        self,
        model: Any,
        entity: AttributeUpdateEntity
    ) -> Any:
        """
        Updates ORM model with values from AttributeUpdateEntity object.

        Parameters:
        - model: ORM model.
        - entity: AttributeUpdateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...

    @abstractmethod
    def update_entities_to_models(
        self,
        models: List[Any],
        entities: List[AttributeUpdateEntity]
    ) -> List[Any]:
        """
        Updates ORM models with values from AttributeUpdateEntity objects.

        Parameters:
        - models: List of ORM models.
        - entities: List of AttributeUpdateEntity objects.

        Returns:
        - List: List of ORM models.
        """
        ...