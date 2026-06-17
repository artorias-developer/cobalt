#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, List, cast, Callable

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from domain.exceptions import (
    ConflictError,
    UnexpectedError
)
from domain.entities import (
    GameEntity,
    GamesPageEntity,
    GamesGetPageEntity,
    GameCreateEntity,
    GameUpdateEntity
)
from domain.repositories import AbstractGamesRepository
from application.contracts.managers import AbstractI18nManager
from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.databases.mappers import AbstractGamesRepositoryMapper
from infrastructure.databases.postgres.models import (
    GameModel,
    LoaderModel
)
from infrastructure.databases.postgres.repositories import BaseRepository
from infrastructure.databases.shared import (
    IntegrityCodesEnum,
    RepositoryOperationsEnum
)


class GamesRepository(AbstractGamesRepository, BaseRepository):
    """
    Repository for working with the 'games' table.
    """
    games_mapper: AbstractGamesRepositoryMapper
    i18n_manager: AbstractI18nManager
    logger: AbstractLogger

    _: Callable

    def __init__(
        self,
        async_session: async_sessionmaker,
        games_mapper: AbstractGamesRepositoryMapper,
        i18n_manager: AbstractI18nManager,
        logger: AbstractLogger
    ):
        super().__init__(async_session)

        self.games_mapper = games_mapper
        self.logger = logger
        self.i18n_manager = i18n_manager

        self._ = i18n_manager.gettext

    def _handle_integrity_error(
        self,
        e: IntegrityError,
        operation: RepositoryOperationsEnum
    ) -> None:
        """
        Handles IntegrityError exceptions for game operations.

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
                game_name = details.get("name")

                raise ConflictError(self._('Game "{name}" already exists').format(name=game_name)) from e

        self.logger.exception(f"Unhandled DB integrity error during {operation}:")
        raise UnexpectedError(self._("Internal server error")) from e

    async def get_page(
        self,
        entity: GamesGetPageEntity,
        session: Optional[AsyncSession] = None
    ) -> GamesPageEntity:
        """
        Gets a paginated list of games.

        Parameters:
        - entity: GamesGetPageEntity object.
        - session: AsyncSession object.

        Returns:
        - GamesPageEntity: GamesPageEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                GameModel
            ).options(
                selectinload(GameModel.loaders)
            )

            if entity.search:
                stmt = stmt.filter(
                    GameModel.name.ilike(f"%{entity.search}%") |
                    GameModel.loaders.any(
                        LoaderModel.name.ilike(f"%{entity.search}%")
                    )
                )

            if entity.sort_field:
                sort_col = getattr(GameModel, entity.sort_field)

                stmt = stmt.order_by(
                    sort_col.desc() if entity.sort_direction == "desc" else sort_col.asc()
                )

            records, total, page, pages = await self.paginate(
                session=session,
                stmt=stmt,
                page=entity.page,
                limit=entity.limit
            )

            records = cast(List[GameModel], records)

            games = self.games_mapper.models_to_entities(
                models=records
            )

            return GamesPageEntity(
                games=games,
                total=total,
                page=page,
                pages=pages
            )

    async def get_one_by_id(
        self,
        game_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[GameEntity]:
        """
        Gets an existing game by ID.

        Parameters:
        - game_id: Game ID.
        - session: AsyncSession object.

        Returns:
        - GameEntity: GameEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                GameModel
            ).options(
                selectinload(GameModel.loaders)
            ).filter(
                GameModel.id == game_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            return self.games_mapper.model_to_entity(
                model=record
            )

    async def get_one_by_name(
        self,
        name: str,
        session: Optional[AsyncSession] = None
    ) -> Optional[GameEntity]:
        """
        Gets an existing game by name.

        Parameters:
        - name: Name of the game.
        - session: AsyncSession object.

        Returns:
        - GameEntity: GameEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                GameModel
            ).options(
                selectinload(GameModel.loaders)
            ).filter(
                GameModel.name == name
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            return self.games_mapper.model_to_entity(
                model=record
            )

    async def create_one(
        self,
        entity: GameCreateEntity,
        session: Optional[AsyncSession] = None
    ) -> GameEntity:
        """
        Creates a new game.

        Parameters:
        - entity: GameCreateEntity object.
        - session: AsyncSession object.

        Returns:
        - GameEntity: GameEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            record = self.games_mapper.create_entity_to_model(
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

            stmt = select(
                GameModel
            ).options(
                selectinload(GameModel.loaders)
            ).filter(
                GameModel.id == record.id
            )

            result = await session.execute(stmt)

            return self.games_mapper.model_to_entity(
                model=result.scalars().first()
            )

    async def update_one(
        self,
        entity: GameUpdateEntity,
        session: Optional[AsyncSession] = None
    ) -> Optional[GameEntity]:
        """
        Updates an existing game.

        Parameters:
        - entity: GameUpdateEntity object.
        - session: AsyncSession object.

        Returns:
        - GameEntity: GameEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                GameModel
            ).options(
                selectinload(GameModel.loaders)
            ).filter(
                GameModel.id == entity.id
            )

            try:
                result = await session.execute(stmt)
                record = result.scalars().first()

                if not record:
                    return None

                record = self.games_mapper.update_entity_to_model(
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

            return self.games_mapper.model_to_entity(
                model=record
            )

    async def delete_one(
        self,
        game_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[GameEntity]:
        """
        Deletes an existing game.

        Parameters:
        - game_id: Game ID.
        - session: AsyncSession object.

        Returns:
        - GameEntity: GameEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                GameModel
            ).options(
                selectinload(GameModel.loaders)
            ).where(
                GameModel.id == game_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            entity = self.games_mapper.model_to_entity(
                model=record
            )

            stmt = delete(
                GameModel
            ).where(
                GameModel.id == game_id
            )

            await session.execute(stmt)

            if not session_provided:
                await session.commit()

            return entity