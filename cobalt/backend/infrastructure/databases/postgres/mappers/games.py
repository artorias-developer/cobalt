#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import GameName
from domain.entities import (
    GameEntity,
    GameCreateEntity,
    GameUpdateEntity
)
from infrastructure.contracts.databases.mappers import (
    AbstractGamesRepositoryMapper,
    AbstractLoadersRepositoryMapper
)
from infrastructure.databases.postgres.models import GameModel


class GamesRepositoryMapper(AbstractGamesRepositoryMapper):
    """
    Games repository mapper.
    """
    loaders_mapper: AbstractLoadersRepositoryMapper

    def __init__(
        self,
        loaders_mapper: AbstractLoadersRepositoryMapper
    ):
        self.loaders_mapper = loaders_mapper

    def model_to_entity(
        self,
        model: GameModel
    ) -> GameEntity:
        """
        Converts GameModel object to GameEntity object.

        Parameters:
        - model: GameModel object.

        Returns:
        - GameEntity: GameEntity object.
        """
        return GameEntity(
            id=model.id,
            name=GameName(model.name),
            loaders=self.loaders_mapper.models_to_entities(
                models=model.loaders
            ),
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def models_to_entities(
        self,
        models: List[GameModel]
    ) -> List[GameEntity]:
        """
        Converts GameModel objects to GameEntity objects.

        Parameters:
        - models: List of GameModel objects.

        Returns:
        - List: List of GameEntity objects.
        """
        return [
            self.model_to_entity(model)
            for model in models
        ]

    def create_entity_to_model(
        self,
        entity: GameCreateEntity
    ) -> GameModel:
        """
        Converts GameCreateEntity object to GameModel object.

        Parameters:
        - entity: GameCreateEntity object.

        Returns:
        - GameModel: GameModel object.
        """
        return GameModel(
            name=entity.name.value
        )

    def update_entity_to_model(
        self,
        model: GameModel,
        entity: GameUpdateEntity
    ) -> GameModel:
        """
        Updates GameModel object with values from GameUpdateEntity object.

        Parameters:
        - model: GameModel object.
        - entity: GameUpdateEntity object.

        Returns:
        - GameModel: GameModel object.
        """
        if entity.name is not None:
            model.name = entity.name.value

        return model