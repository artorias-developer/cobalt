#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from domain.entities import (
    ServerEntity,
    ServerCreateEntity,
    ServerUpdateEntity
)


class AbstractServersRepositoryMapper(ABC):
    """
    Abstract servers repository mapper.
    """

    @abstractmethod
    def model_to_entity(
        self,
        model: Any
    ) -> ServerEntity:
        """
        Converts ORM model to ServerEntity object.

        Parameters:
        - model: ORM model.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        ...

    @abstractmethod
    def models_to_entities(
        self,
        models: List[Any]
    ) -> List[ServerEntity]:
        """
        Converts ORM models to ServerEntity objects.

        Parameters:
        - models: List of ORM models.

        Returns:
        - List: List of ServerEntity objects.
        """
        ...

    @abstractmethod
    def create_entity_to_model(
        self,
        entity: ServerCreateEntity
    ) -> Any:
        """
        Converts ServerCreateEntity object to ORM model.

        Parameters:
        - entity: ServerCreateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...

    @abstractmethod
    def update_entity_to_model(
        self,
        model: Any,
        entity: ServerUpdateEntity
    ) -> Any:
        """
        Updates ORM model with data from ServerUpdateEntity object.

        Parameters:
        - model: ORM model.
        - entity: ServerUpdateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...