#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.dtos import (
    SettingsDto,
    SettingsUpdateDto
)
from presentation.contracts.http.mappers import AbstractSettingsRouterMapper
from presentation.http.fastapi.v1.schemas import (
    SettingsSchema,
    SettingsUpdateSchema
)


class SettingsRouterMapper(AbstractSettingsRouterMapper):
    """
    Mapper for settings router.
    """

    def dto_to_schema(
        self,
        dto: SettingsDto
    ) -> SettingsSchema:
        """
        Converts SettingsDto object to SettingsSchema object.

        Parameters:
        - dto: SettingsDto object.

        Returns:
        - SettingsSchema: SettingsSchema object.
        """
        return SettingsSchema(
            id=dto.id,
            user_id=dto.user_id,
            language=dto.language,
            theme=dto.theme,
            timezone=dto.timezone,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    def update_schema_to_dto(
        self,
        schema: SettingsUpdateSchema
    ) -> SettingsUpdateDto:
        """
        Converts SettingsUpdateSchema object to SettingsUpdateDto object.

        Parameters:
        - schema: SettingsUpdateSchema object.

        Returns:
        - SettingsUpdateDto: SettingsUpdateDto object.
        """
        return SettingsUpdateDto(
            language=schema.language,
            theme=schema.theme,
            timezone=schema.timezone
        )