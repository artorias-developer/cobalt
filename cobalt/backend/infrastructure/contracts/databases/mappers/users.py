#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from domain.entities import (
    UserEntity,
    UserCreateEntity,
    UserUpdateEntity
)


class AbstractUsersRepositoryMapper(ABC):
    """
    Abstract users repository mapper.
    """

    @abstractmethod
    def model_to_entity(
        self,
        model: Any
    ) -> UserEntity:
        """
        Converts ORM model to UserEntity object.

        Parameters:
        - model: ORM model.

        Returns:
        - UserEntity: UserEntity object.
        """
        ...

    @abstractmethod
    def models_to_entities(
        self,
        models: List[Any]
    ) -> List[UserEntity]:
        """
        Converts ORM models to UserEntity objects.

        Parameters:
        - models: List of ORM models.

        Returns:
        - List: List of UserEntity objects.
        """
        ...

    @abstractmethod
    def create_entity_to_model(
        self,
        entity: UserCreateEntity
    ) -> Any:
        """
        Converts UserCreateEntity object to ORM model.

        Parameters:
        - entity: UserCreateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...

    @abstractmethod
    def update_entity_to_model(
        self,
        model: Any,
        entity: UserUpdateEntity
    ) -> Any:
        """
        Updates ORM model with data from UserUpdateEntity object.

        Parameters:
        - model: ORM model.
        - entity: UserUpdateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...