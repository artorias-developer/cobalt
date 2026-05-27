#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod

from domain.entities import (
    SettingsEntity,
    SettingsUpdateEntity
)
from application.dtos import (
    SettingsDto,
    SettingsUpdateDto
)


class AbstractSettingsServiceMapper(ABC):
    """
    Abstract mapper for settings service.
    """

    @abstractmethod
    def entity_to_dto(
        self,
        entity: SettingsEntity
    ) -> SettingsDto:
        """
        Converts SettingsEntity object to SettingsDto object.

        Parameters:
        - entity: SettingsEntity object.

        Returns:
        - SettingsDto: SettingsDto object.
        """
        ...

    @abstractmethod
    def update_dto_to_entity(
        self,
        dto: SettingsUpdateDto
    ) -> SettingsUpdateEntity:
        """
        Converts SettingsUpdateDto object to SettingsUpdateEntity object.

        Parameters:
        - dto: SettingsUpdateDto object.

        Returns:
        - SettingsUpdateEntity: SettingsUpdateEntity object.
        """
        ...