#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from domain.entities import (
    SettingsEntity,
    SettingsUpdateEntity
)
from domain.repositories import AbstractSettingsRepository
from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.databases.mappers import AbstractSettingsRepositoryMapper
from infrastructure.databases.postgres.models import SettingsModel
from infrastructure.databases.postgres.repositories import BaseRepository


class SettingsRepository(AbstractSettingsRepository, BaseRepository):
    """
    Repository for working with the 'users_settings' table.
    """
    settings_mapper: AbstractSettingsRepositoryMapper
    logger: AbstractLogger

    def __init__(
        self,
        async_session: async_sessionmaker,
        settings_mapper: AbstractSettingsRepositoryMapper,
        logger: AbstractLogger
    ):
        super().__init__(async_session)
        
        self.settings_mapper = settings_mapper
        self.logger = logger

    async def update_one(
        self,
        user_id: int,
        entity: SettingsUpdateEntity,
        session: Optional[AsyncSession] = None
    ) -> Optional[SettingsEntity]:
        """
        Updates existing settings.

        Parameters:
        - user_id: User ID.
        - entity: SettingsUpdateEntity object.
        - session: AsyncSession object.

        Returns:
        - SettingsEntity: SettingsEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                SettingsModel
            ).filter(
                SettingsModel.user_id == user_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            record = self.settings_mapper.update_entity_to_model(
                model=record,
                entity=entity
            )

            if session_provided:
                await session.flush()
            else:
                await session.commit()

            return self.settings_mapper.model_to_entity(
                model=record
            )