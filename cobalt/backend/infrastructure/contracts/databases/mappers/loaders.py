#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from domain.entities import (
    LoaderEntity,
    LoaderCreateEntity,
    LoaderUpdateEntity
)


class AbstractLoadersRepositoryMapper(ABC):
    """
    Abstract loaders repository mapper.
    """

    @abstractmethod
    def model_to_entity(
        self,
        model: Any
    ) -> LoaderEntity:
        """
        Converts ORM model to LoaderEntity object.

        Parameters:
        - model: ORM model.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        ...

    @abstractmethod
    def models_to_entities(
        self,
        models: List[Any]
    ) -> List[LoaderEntity]:
        """
        Converts ORM models to LoaderEntity objects.

        Parameters:
        - models: List of ORM models.

        Returns:
        - List: List of LoaderEntity objects.
        """
        ...

    @abstractmethod
    def create_entity_to_model(
        self,
        game_id: int,
        entity: LoaderCreateEntity
    ) -> Any:
        """
        Converts LoaderCreateEntity object to ORM model.

        Parameters:
        - game_id: Game ID.
        - entity: LoaderCreateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...

    @abstractmethod
    def update_entity_to_model(
        self,
        model: Any,
        entity: LoaderUpdateEntity
    ) -> Any:
        """
        Updates ORM model with data from LoaderUpdateEntity object.

        Parameters:
        - model: ORM model.
        - entity: LoaderUpdateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...
