#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any

from domain.entities import SettingsEntity, SettingsUpdateEntity


class AbstractSettingsRepositoryMapper(ABC):
    """
    Abstract settings repository mapper.
    """

    @abstractmethod
    def model_to_entity(
        self,
        model: Any
    ) -> SettingsEntity:
        """
        Converts ORM model to SettingsEntity object.

        Parameters:
        - model: ORM model.

        Returns:
        - SettingsEntity: SettingsEntity object.
        """
        ...

    @abstractmethod
    def update_entity_to_model(
        self,
        model: Any,
        entity: SettingsUpdateEntity
    ) -> Any:
        """
        Updates ORM model with data from SettingsUpdateEntity object.

        Parameters:
        - model: ORM model.
        - entity: SettingsUpdateEntity object.

        Returns:
        - Any: ORM model.
        """
        ...