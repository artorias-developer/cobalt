#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import LoaderName
from domain.entities import (
    LoaderEntity,
    LoaderCreateEntity,
    LoaderUpdateEntity
)
from infrastructure.contracts.databases.mappers import AbstractLoadersRepositoryMapper
from infrastructure.databases.postgres.models import LoaderModel


class LoadersRepositoryMapper(AbstractLoadersRepositoryMapper):
    """
    Loaders repository mapper.
    """

    def model_to_entity(
        self,
        model: LoaderModel
    ) -> LoaderEntity:
        """
        Converts LoaderModel object to LoaderEntity object.

        Parameters:
        - model: LoaderModel object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        return LoaderEntity(
            id=model.id,
            game_id=model.game_id,
            name=LoaderName(model.name),
            versions=model.versions,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def models_to_entities(
        self,
        models: List[LoaderModel]
    ) -> List[LoaderEntity]:
        """
        Converts LoaderModel objects to LoaderEntity objects.

        Parameters:
        - models: List of LoaderModel objects.

        Returns:
        - List: List of LoaderEntity objects.
        """
        return [
            self.model_to_entity(model)
            for model in models
        ]

    def create_entity_to_model(
        self,
        game_id: int,
        entity: LoaderCreateEntity
    ) -> LoaderModel:
        """
        Converts LoaderCreateEntity object to LoaderModel object.

        Parameters:
        - game_id: Game ID.
        - entity: LoaderCreateEntity object.

        Returns:
        - LoaderModel: LoaderModel object.
        """
        return LoaderModel(
            game_id=game_id,
            name=entity.name,
            versions=entity.versions
        )

    def update_entity_to_model(
        self,
        model: LoaderModel,
        entity: LoaderUpdateEntity
    ) -> LoaderModel:
        """
        Updates LoaderModel object with data from LoaderUpdateEntity object.

        Parameters:
        - model: LoaderModel object.
        - entity: LoaderUpdateEntity object.

        Returns:
        - LoaderModel: LoaderModel object.
        """
        if entity.name is not None:
            model.name = entity.name

        if entity.versions is not None:
            model.versions = entity.versions

        return model