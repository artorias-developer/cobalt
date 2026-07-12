#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, Callable

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from domain.exceptions import (
    ConflictError,
    UnexpectedError
)
from domain.entities import (
    LoaderEntity,
    LoaderCreateEntity,
    LoaderUpdateEntity
)
from domain.repositories import AbstractLoadersRepository
from application.contracts.managers import AbstractI18nManager
from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.databases.mappers import AbstractLoadersRepositoryMapper
from infrastructure.databases.postgres.models import LoaderModel
from infrastructure.databases.postgres.repositories import BaseRepository
from infrastructure.databases.shared import (
    IntegrityCodesEnum,
    RepositoryOperationsEnum
)


class LoadersRepository(AbstractLoadersRepository, BaseRepository):
    """
    Repository for working with the 'games_loaders' table.
    """
    loaders_mapper: AbstractLoadersRepositoryMapper
    i18n_manager: AbstractI18nManager
    logger: AbstractLogger

    _: Callable

    def __init__(
        self,
        async_session: async_sessionmaker,
        loaders_mapper: AbstractLoadersRepositoryMapper,
        i18n_manager: AbstractI18nManager,
        logger: AbstractLogger
    ):
        super().__init__(async_session)

        self.loaders_mapper = loaders_mapper
        self.i18n_manager = i18n_manager
        self.logger = logger

        self._ = i18n_manager.gettext

    def _handle_integrity_error(
        self,
        e: IntegrityError,
        operation: RepositoryOperationsEnum
    ) -> None:
        """
        Handles IntegrityError exceptions for loader operations.

        Parameters:
        - e: The IntegrityError exception.
        - operation: The operation that caused the error.

        Returns:
        - None.
        """
        sqlstate = getattr(e.orig, "sqlstate", None)
        details = self.parse_asyncpg_detail_to_dict(e)

        if sqlstate == IntegrityCodesEnum.UNIQUE_VIOLATION:
            if operation in [
                RepositoryOperationsEnum.CREATE,
                RepositoryOperationsEnum.UPDATE
            ]:
                loader_name = details.get("name")

                raise ConflictError(self._('Loader "{name}" already exists').format(name=loader_name)) from e

        self.logger.exception(f"Unhandled DB integrity error during {operation}:")
        raise UnexpectedError(self._("Internal server error")) from e

    async def get_one_by_id(
        self,
        loader_id: int,
        game_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[LoaderEntity]:
        """
        Gets an existing loader by ID.

        Parameters:
        - loader_id: Loader ID.
        - game_id: Game ID.
        - session: AsyncSession object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                LoaderModel
            ).filter(
                LoaderModel.id == loader_id,
                LoaderModel.game_id == game_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            return self.loaders_mapper.model_to_entity(
                model=record
            )

    async def get_one_by_name(
        self,
        name: str,
        game_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[LoaderEntity]:
        """
        Gets an existing loader by name.

        Parameters:
        - name: Name of the loader.
        - game_id: Game Loader ID.
        - session: AsyncSession object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                LoaderModel
            ).filter(
                LoaderModel.name == name,
                LoaderModel.game_id == game_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            return self.loaders_mapper.model_to_entity(
                model=record
            )

    async def create_one(
        self,
        game_id: int,
        entity: LoaderCreateEntity,
        session: Optional[AsyncSession] = None
    ) -> LoaderEntity:
        """
        Creates a new loader.

        Parameters:
        - game_id: Game ID.
        - entity: LoaderCreateEntity object.
        - session: AsyncSession object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            record = self.loaders_mapper.create_entity_to_model(
                game_id=game_id,
                entity=entity
            )

            try:
                session.add(record)

                if session_provided:
                    await session.flush()
                else:
                    await session.commit()

            except IntegrityError as e:
                if not session_provided:
                    await session.rollback()

                self._handle_integrity_error(
                    e=e,
                    operation=RepositoryOperationsEnum.CREATE
                )

            return self.loaders_mapper.model_to_entity(
                model=record
            )

    async def update_one(
        self,
        game_id: int,
        entity: LoaderUpdateEntity,
        session: Optional[AsyncSession] = None
    ) -> Optional[LoaderEntity]:
        """
        Updates an existing loader.

        Parameters:
        - game_id: Game ID.
        - entity: LoaderUpdateEntity object.
        - session: AsyncSession object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                LoaderModel
            ).filter(
                LoaderModel.id == entity.id,
                LoaderModel.game_id == game_id
            )

            try:
                result = await session.execute(stmt)
                record = result.scalars().first()

                if not record:
                    return None

                record = self.loaders_mapper.update_entity_to_model(
                    model=record,
                    entity=entity
                )

                if session_provided:
                    await session.flush()
                else:
                    await session.commit()

            except IntegrityError as e:
                if not session_provided:
                    await session.rollback()

                self._handle_integrity_error(
                    e=e,
                    operation=RepositoryOperationsEnum.UPDATE
                )

            return self.loaders_mapper.model_to_entity(
                model=record
            )

    async def delete_one(
        self,
        game_id: int,
        loader_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[LoaderEntity]:
        """
        Deletes an existing loader.

        Parameters:
        - game_id: Game ID.
        - loader_id: Loader ID.
        - session: AsyncSession object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = delete(
                LoaderModel
            ).where(
                LoaderModel.id == loader_id,
                LoaderModel.game_id == game_id
            ).returning(
                LoaderModel
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            if not session_provided:
                await session.commit()

            return self.loaders_mapper.model_to_entity(
                model=record
            )