#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import (
    UserLogin,
    HashedPassword,
    Salt
)
from domain.entities import (
    UserEntity,
    UserCreateEntity,
    UserUpdateEntity
)
from infrastructure.contracts.databases.mappers import (
    AbstractUsersRepositoryMapper,
    AbstractRolesRepositoryMapper,
    AbstractSettingsRepositoryMapper
)
from infrastructure.databases.postgres.models import UserModel


class UsersRepositoryMapper(AbstractUsersRepositoryMapper):
    """
    Users repository mapper.
    """
    roles_mapper: AbstractRolesRepositoryMapper
    settings_mapper: AbstractSettingsRepositoryMapper

    def __init__(
        self,
        roles_mapper: AbstractRolesRepositoryMapper,
        settings_mapper: AbstractSettingsRepositoryMapper
    ):
        self.roles_mapper = roles_mapper
        self.settings_mapper = settings_mapper

    def model_to_entity(
        self,
        model: UserModel
    ) -> UserEntity:
        """
        Converts UserModel object to UserEntity object.

        Parameters:
        - model: UserModel object.

        Returns:
        - UserEntity: UserEntity object.
        """
        return UserEntity(
            id=model.id,
            login=UserLogin(model.login),
            hashed_password=HashedPassword(model.hashed_password),
            salt=Salt(model.salt),
            role=self.roles_mapper.model_to_entity(
                model=model.role
            ),
            settings=self.settings_mapper.model_to_entity(
                model=model.settings
            ),
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def models_to_entities(
        self,
        models: List[UserModel]
    ) -> List[UserEntity]:
        """
        Converts UserModel objects to UserEntity objects.

        Parameters:
        - models: List of UserModel objects.

        Returns:
        - List: List of UserEntity objects.
        """
        return [
            self.model_to_entity(model)
            for model in models
        ]

    def create_entity_to_model(
        self,
        entity: UserCreateEntity
    ) -> UserModel:
        """
        Converts UserCreateEntity object to UserModel object.

        Parameters:
        - entity: UserCreateEntity object.

        Returns:
        - UserModel: UserModel object.
        """
        return UserModel(
            login=entity.login,
            hashed_password=entity.hashed_password,
            salt=entity.salt,
            role_id=entity.role_id
        )

    def update_entity_to_model(
        self,
        model: UserModel,
        entity: UserUpdateEntity
    ) -> UserModel:
        """
        Updates UserModel object with data from UserUpdateEntity object.

        Parameters:
        - model: UserModel object.
        - entity: UserUpdateEntity object.

        Returns:
        - UserModel: UserModel object.
        """
        if entity.login is not None:
            model.login = entity.login

        if entity.hashed_password is not None:
            model.hashed_password = entity.hashed_password

        if entity.salt is not None:
            model.salt = entity.salt

        if entity.role_id is not None:
            model.role_id = entity.role_id

        return model