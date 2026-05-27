#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import RoleName
from domain.entities import (
    RoleEntity,
    RoleCreateEntity,
    RoleUpdateEntity
)
from infrastructure.contracts.databases.mappers import AbstractRolesRepositoryMapper
from infrastructure.databases.postgres.models import RoleModel


class RolesRepositoryMapper(AbstractRolesRepositoryMapper):
    """
    Roles repository mapper.
    """

    def model_to_entity(
        self,
        model: RoleModel
    ) -> RoleEntity:
        """
        Converts RoleModel object to RoleEntity object.

        Parameters:
        - model: RoleModel object.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        return RoleEntity(
            id=model.id,
            name=RoleName(model.name),
            permissions=model.permissions,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def models_to_entities(
        self,
        models: List[RoleModel]
    ) -> List[RoleEntity]:
        """
        Converts RoleModel objects to RoleEntity objects.

        Parameters:
        - models: List of RoleModel objects.

        Returns:
        - List: List of RoleEntity objects.
        """
        return [
            self.model_to_entity(model)
            for model in models
        ]

    def create_entity_to_model(
        self,
        entity: RoleCreateEntity
    ) -> RoleModel:
        """
        Converts RoleCreateEntity object to RoleModel object.

        Parameters:
        - entity: RoleCreateEntity object.

        Returns:
        - RoleModel: RoleModel object.
        """
        return RoleModel(
            name=entity.name,
            permissions=entity.permissions
        )

    def update_entity_to_model(
        self,
        model: RoleModel,
        entity: RoleUpdateEntity
    ) -> RoleModel:
        """
        Updates RoleModel object with data from RoleUpdateEntity object.

        Parameters:
        - model: RoleModel object.
        - entity: RoleUpdateEntity object.

        Returns:
        - RoleModel: RoleModel object.
        """
        if entity.name is not None:
            model.name = entity.name

        if entity.permissions is not None:
            model.permissions = entity.permissions

        return model