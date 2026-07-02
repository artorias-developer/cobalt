#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import AttributeKey
from domain.entities import (
    AttributeEntity,
    AttributeCreateEntity,
    AttributeUpdateEntity
)
from infrastructure.contracts.databases.mappers import AbstractAttributesRepositoryMapper
from infrastructure.databases.postgres.models import AttributeModel


class AttributesRepositoryMapper(AbstractAttributesRepositoryMapper):
    """
    Attributes repository mapper.
    """

    def model_to_entity(
        self,
        model: AttributeModel
    ) -> AttributeEntity:
        """
        Converts AttributeModel object to AttributeEntity object.

        Parameters:
        - model: AttributeModel object.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        return AttributeEntity(
            id=model.id,
            server_id=model.server_id,
            key=AttributeKey(model.key),
            value=model.value,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def models_to_entities(
        self,
        models: List[AttributeModel]
    ) -> List[AttributeEntity]:
        """
        Converts AttributeModel objects to AttributeEntity objects.

        Parameters:
        - models: List of AttributeModel objects.

        Returns:
        - List: List of AttributeEntity objects.
        """
        return [
            self.model_to_entity(model)
            for model in models
        ]

    def create_entity_to_model(
        self,
        server_id: int,
        entity: AttributeCreateEntity
    ) -> AttributeModel:
        """
        Converts AttributeCreateEntity object to AttributeModel object.

        Parameters:
        - server_id: Server ID.
        - entity: AttributeCreateEntity object.

        Returns:
        - AttributeModel: AttributeModel object.
        """
        return AttributeModel(
            server_id=server_id,
            key=entity.key.value,
            value=entity.value
        )

    def create_entities_to_models(
        self,
        server_id: int,
        entities: List[AttributeCreateEntity]
    ) -> List[AttributeModel]:
        """
        Converts AttributeCreateEntity objects to AttributeModel objects.

        Parameters:
        - server_id: Server ID.
        - entities: List of AttributeCreateEntity objects.

        Returns:
        - List: List of AttributeModel objects.
        """
        return [
            self.create_entity_to_model(server_id, entity)
            for entity in entities
        ]

    def update_entity_to_model(
        self,
        model: AttributeModel,
        entity: AttributeUpdateEntity
    ) -> AttributeModel:
        """
        Updates AttributeModel object with values from AttributeUpdateEntity object.

        Parameters:
        - model: AttributeModel object.
        - entity: AttributeUpdateEntity object.

        Returns:
        - AttributeModel: AttributeModel object.
        """
        if entity.value is not None:
            model.value = entity.value

        return model

    def update_entities_to_models(
        self,
        models: List[AttributeModel],
        entities: List[AttributeUpdateEntity]
    ) -> List[AttributeModel]:
        """
        Updates AttributeModel objects with values from AttributeUpdateEntity objects.

        Parameters:
        - models: List of AttributeModel objects.
        - entities: List of AttributeUpdateEntity objects.

        Returns:
        - List: List of AttributeModel objects.
        """
        mapped_models = {
            model.id: model
            for model in models
        }

        updated_models = []

        for entity in entities:
            model = mapped_models.get(entity.id)

            if not model:
                continue

            model = self.update_entity_to_model(
                model=model,
                entity=entity
            )

            updated_models.append(model)

        return updated_models