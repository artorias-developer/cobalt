#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from domain.entities import (
    RoleEntity,
    RoleCreateEntity,
    RoleUpdateEntity
)


class AbstractRolesRepositoryMapper(ABC):
    """
    Abstract roles repository mapper.
    """

    @abstractmethod
    def model_to_entity(
        self,
        model: Any
    ) -> RoleEntity:
        """
        Converts ORM model to RoleEntity object.

        Parameters:
        - model: ORM model.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        ...

    @abstractmethod
    def models_to_entities(
        self,
        models: List[Any]
    ) -> List[RoleEntity]:
        """
        Converts ORM models to RoleEntity objects.

        Parameters:
        - models: List of ORM models.

        Returns:
        - List: List of RoleEntity objects.
        """
        ...

    @abstractmethod
    def create_entity_to_model(
        self,
        entity: RoleCreateEntity
    ) -> Any:
        """
        Converts RoleCreateEntity object to ORM model.

        Parameters:
        - entity: RoleCreateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...

    @abstractmethod
    def update_entity_to_model(
        self,
        model: Any,
        entity: RoleUpdateEntity
    ) -> Any:
        """
        Updates ORM model with data from RoleUpdateEntity object.

        Parameters:
        - model: ORM model.
        - entity: RoleUpdateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...
