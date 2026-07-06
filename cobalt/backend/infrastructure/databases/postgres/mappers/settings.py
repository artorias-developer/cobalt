#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from domain.entities import SettingsEntity, SettingsUpdateEntity
from infrastructure.contracts.databases.mappers import AbstractSettingsRepositoryMapper
from infrastructure.databases.postgres.models import SettingsModel


class SettingsRepositoryMapper(AbstractSettingsRepositoryMapper):
    """
    Settings repository mapper.
    """

    def model_to_entity(
        self,
        model: SettingsModel
    ) -> SettingsEntity:
        """
        Converts SettingsModel object to SettingsEntity object.

        Parameters:
        - model: SettingsModel object.

        Returns:
        - SettingsEntity: SettingsEntity object.
        """
        return SettingsEntity(
            id=model.id,
            user_id=model.user_id,
            language=model.language,
            theme=model.theme,
            timezone=model.timezone,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def update_entity_to_model(
        self,
        model: SettingsModel,
        entity: SettingsUpdateEntity
    ) -> SettingsModel:
        """
        Updates SettingsModel object with data from SettingsUpdateEntity object.

        Parameters:
        - model: SettingsModel object.
        - entity: SettingsUpdateEntity object.

        Returns:
        - SettingsModel: SettingsModel object.
        """
        if entity.language is not None:
            model.language = entity.language

        if entity.theme is not None:
            model.theme = entity.theme

        if entity.timezone is not None:
            model.timezone = entity.timezone

        return model