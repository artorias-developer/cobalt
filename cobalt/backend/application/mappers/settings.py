#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from domain.entities import (
    SettingsEntity,
    SettingsUpdateEntity
)
from application.contracts.mappers import AbstractSettingsServiceMapper
from application.dtos import (
    SettingsDto,
    SettingsUpdateDto
)


class SettingsServiceMapper(AbstractSettingsServiceMapper):
    """
    Mapper for settings service.
    """

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
        return SettingsDto(
            id=entity.id,
            user_id=entity.id,
            language=entity.language,
            theme=entity.theme,
            timezone=entity.timezone,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

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
        return SettingsUpdateEntity(
            language=dto.language,
            theme=dto.theme,
            timezone=dto.timezone
        )