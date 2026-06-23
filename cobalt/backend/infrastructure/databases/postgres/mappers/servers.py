#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import (
    ServerName,
    ServerVersion
)
from domain.entities import (
    ServerEntity,
    ServerCreateEntity,
    ServerUpdateEntity
)
from domain.enums import ServerStatusEnum
from infrastructure.contracts.databases.mappers import (
    AbstractServersRepositoryMapper,
    AbstractAttributesRepositoryMapper,
    AbstractGamesRepositoryMapper,
    AbstractLoadersRepositoryMapper
)
from infrastructure.databases.postgres.models import ServerModel


class ServersRepositoryMapper(AbstractServersRepositoryMapper):
    """
    Servers repository mapper.
    """
    attributes_mapper: AbstractAttributesRepositoryMapper
    games_mapper: AbstractGamesRepositoryMapper
    loaders_mapper: AbstractLoadersRepositoryMapper

    def __init__(
        self,
        attributes_mapper: AbstractAttributesRepositoryMapper,
        games_mapper: AbstractGamesRepositoryMapper,
        loaders_mapper: AbstractLoadersRepositoryMapper
    ):
        self.attributes_mapper = attributes_mapper
        self.games_mapper = games_mapper
        self.loaders_mapper = loaders_mapper

    def model_to_entity(
        self,
        model: ServerModel
    ) -> ServerEntity:
        """
        Converts ServerModel object to ServerEntity object.

        Parameters:
        - model: ServerModel object.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        return ServerEntity(
            id=model.id,
            name=ServerName(model.name),
            version=ServerVersion(model.version),
            game=self.games_mapper.model_to_entity(
                model=model.game
            ),
            loader=self.loaders_mapper.model_to_entity(
                model=model.loader
            ),
            attributes=self.attributes_mapper.models_to_entities(
                models=model.attributes
            ),
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def models_to_entities(
        self,
        models: List[ServerModel]
    ) -> List[ServerEntity]:
        """
        Converts ServerModel objects to ServerEntity objects.

        Parameters:
        - models: List of ServerModel objects.

        Returns:
        - List: List of ServerEntity objects.
        """
        return [
            self.model_to_entity(model)
            for model in models
        ]

    def create_entity_to_model(
        self,
        entity: ServerCreateEntity
    ) -> ServerModel:
        """
        Converts ServerCreateEntity object to ServerModel object.

        Parameters:
        - entity: ServerCreateEntity object.

        Returns:
        - ServerModel: ServerModel object.
        """
        return ServerModel(
            name=entity.name,
            game_id=entity.game_id,
            loader_id=entity.loader_id,
            version=entity.version,
            status=ServerStatusEnum.PENDING
        )

    def update_entity_to_model(
        self,
        model: ServerModel,
        entity: ServerUpdateEntity
    ) -> ServerModel:
        """
        Updates ServerModel object with data from ServerUpdateEntity object.

        Parameters:
        - model: ServerModel object.
        - entity: ServerUpdateEntity object.

        Returns:
        - ServerModel: ServerModel object.
        """
        if entity.name is not None:
            model.name = entity.name

        if entity.version is not None:
            model.version = entity.version

        if entity.status is not None:
            model.status = entity.status

        return model