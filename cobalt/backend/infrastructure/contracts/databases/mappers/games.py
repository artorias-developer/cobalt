#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from domain.entities import (
    GameEntity,
    GameCreateEntity,
    GameUpdateEntity
)


class AbstractGamesRepositoryMapper(ABC):
    """
    Abstract games repository mapper.
    """

    @abstractmethod
    def model_to_entity(
        self,
        model: Any
    ) -> GameEntity:
        """
        Converts ORM model to GameEntity object.

        Parameters:
        - model: ORM model.

        Returns:
        - GameEntity: GameEntity object.
        """
        ...

    @abstractmethod
    def models_to_entities(
        self,
        models: List[Any]
    ) -> List[GameEntity]:
        """
        Converts ORM models to GameEntity objects.

        Parameters:
        - models: List of ORM models.

        Returns:
        - List: List of GameEntity objects.
        """
        ...

    @abstractmethod
    def create_entity_to_model(
        self,
        entity: GameCreateEntity
    ) -> Any:
        """
        Converts GameCreateEntity object to ORM model.

        Parameters:
        - entity: GameCreateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...

    @abstractmethod
    def update_entity_to_model(
        self,
        model: Any,
        entity: GameUpdateEntity
    ) -> Any:
        """
        Updates ORM model with values from GameUpdateEntity object.

        Parameters:
        - model: ORM model.
        - entity: GameUpdateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...