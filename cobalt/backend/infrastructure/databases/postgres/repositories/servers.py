#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, List, cast, Callable

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from domain.entities import (
    ServerEntity,
    ServersPageEntity,
    ServersGetPageEntity,
    ServerCreateEntity,
    ServerUpdateEntity
)
from domain.exceptions import (
    ConflictError,
    UnexpectedError,
    NotFoundError
)
from domain.repositories import AbstractServersRepository
from application.contracts.managers import AbstractI18nManager
from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.databases.mappers import AbstractServersRepositoryMapper
from infrastructure.databases.postgres.models import (
    ServerModel,
    GameModel,
    LoaderModel
)
from infrastructure.databases.postgres.repositories import BaseRepository
from infrastructure.databases.shared import (
    IntegrityCodesEnum,
    RepositoryOperationsEnum
)


class ServersRepository(AbstractServersRepository, BaseRepository):
    """
    Repository for working with the 'servers' table.
    """
    servers_mapper: AbstractServersRepositoryMapper
    i18n_manager: AbstractI18nManager
    logger: AbstractLogger

    _: Callable

    def __init__(
        self,
        async_session: async_sessionmaker,
        servers_mapper: AbstractServersRepositoryMapper,
        i18n_manager: AbstractI18nManager,
        logger: AbstractLogger
    ):
        super().__init__(async_session)

        self.servers_mapper = servers_mapper
        self.i18n_manager = i18n_manager
        self.logger = logger

        self._ = i18n_manager.gettext

    def _handle_integrity_error(
        self,
        e: IntegrityError,
        operation: RepositoryOperationsEnum
    ) -> None:
        """
        Handles IntegrityError exceptions for server operations.

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
                server_name = details.get("name")

                raise ConflictError(self._('Server "{name}" already exists').format(name=server_name)) from e

        if sqlstate == IntegrityCodesEnum.FOREIGN_KEY_VIOLATION:
            if operation == RepositoryOperationsEnum.CREATE:
                game_id = details.get("game_id")
                loader_id = details.get("loader_id")

                raise NotFoundError(
                    self._("Game {game_id} or loader {loader_id} not found").format(
                        game_id=game_id,
                        loader_id=loader_id
                    )
                ) from e

        self.logger.exception(f"Unhandled DB integrity error during {operation}:")
        raise UnexpectedError(self._("Internal server error")) from e

    async def get_page(
        self,
        entity: ServersGetPageEntity,
        session: Optional[AsyncSession] = None
    ) -> ServersPageEntity:
        """
        Gets a paginated list of servers.

        Parameters:
        - entity: ServersGetPageEntity object.
        - session: AsyncSession object.

        Returns:
        - ServersPageEntity: ServersPageEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                ServerModel
            ).options(
                joinedload(ServerModel.game).selectinload(GameModel.loaders),
                joinedload(ServerModel.loader),
                selectinload(ServerModel.attributes)
            )

            if entity.search:
                stmt = stmt.filter(
                    ServerModel.name.ilike(f"%{entity.search}%") |
                    ServerModel.version.ilike(f"%{entity.search}%") |
                    ServerModel.game.has(
                        GameModel.name.ilike(f"%{entity.search}%")
                    ) |
                    ServerModel.loader.has(
                        LoaderModel.name.ilike(f"%{entity.search}%")
                    )
                )

            if entity.sort_field:
                sort_col = getattr(ServerModel, entity.sort_field)

                stmt = stmt.order_by(
                    sort_col.desc() if entity.sort_direction == "desc" else sort_col.asc()
                )

            records, total, page, pages = await self.paginate(
                session=session,
                stmt=stmt,
                page=entity.page,
                limit=entity.limit
            )

            records = cast(List[ServerModel], records)

            servers = self.servers_mapper.models_to_entities(
                models=records
            )

            return ServersPageEntity(
                servers=servers,
                total=total,
                page=page,
                pages=pages
            )

    async def get_one_by_id(
        self,
        server_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[ServerEntity]:
        """
        Gets an existing server by ID.

        Parameters:
        - server_id: Server ID.
        - session: AsyncSession object.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                ServerModel
            ).options(
                joinedload(ServerModel.game).selectinload(GameModel.loaders),
                joinedload(ServerModel.loader),
                selectinload(ServerModel.attributes)
            ).filter(
                ServerModel.id == server_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            return self.servers_mapper.model_to_entity(
                model=record
            )

    async def get_many_by_ids(
        self,
        server_ids: List[int],
        session: Optional[AsyncSession] = None
    ) -> List[ServerEntity]:
        """
        Gets multiple existing servers by IDs.

        Parameters:
        - server_ids: List of server IDs.
        - session: AsyncSession object.

        Returns:
        - List: List of ServerEntity objects.
        """
        async with self._get_session(session) as session:
            stmt = select(
                ServerModel
            ).options(
                joinedload(ServerModel.game).selectinload(GameModel.loaders),
                joinedload(ServerModel.loader),
                selectinload(ServerModel.attributes)
            ).where(
                ServerModel.id.in_(server_ids)
            )

            result = await session.execute(stmt)
            records = cast(List[ServerModel], result.scalars().all())

            return self.servers_mapper.models_to_entities(
                models=records
            )

    async def create_one(
        self,
        entity: ServerCreateEntity,
        session: Optional[AsyncSession] = None
    ) -> ServerEntity:
        """
        Creates a new server.

        Parameters:
        - entity: ServerCreateEntity object.
        - session: AsyncSession object.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            record = self.servers_mapper.create_entity_to_model(
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
                ServerModel
            ).options(
                joinedload(ServerModel.game).selectinload(GameModel.loaders),
                joinedload(ServerModel.loader),
                selectinload(ServerModel.attributes)
            ).filter(
                ServerModel.id == record.id
            )

            result = await session.execute(stmt)

            return self.servers_mapper.model_to_entity(
                model=result.scalars().first()
            )

    async def update_one(
        self,
        entity: ServerUpdateEntity,
        session: Optional[AsyncSession] = None
    ) -> Optional[ServerEntity]:
        """
        Updates an existing server.

        Parameters:
        - entity: ServerUpdateEntity object.
        - session: AsyncSession object.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                ServerModel
            ).options(
                joinedload(ServerModel.game).selectinload(GameModel.loaders),
                joinedload(ServerModel.loader),
                selectinload(ServerModel.attributes)
            ).filter(
                ServerModel.id == entity.id
            )

            try:
                result = await session.execute(stmt)
                record = result.scalars().first()

                if not record:
                    return None

                record = self.servers_mapper.update_entity_to_model(
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

            return self.servers_mapper.model_to_entity(
                model=record
            )

    async def delete_one(
        self,
        server_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[ServerEntity]:
        """
        Deletes an existing server.

        Parameters:
        - server_id: Server ID.
        - session: AsyncSession object.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                ServerModel
            ).options(
                joinedload(ServerModel.game).selectinload(GameModel.loaders),
                joinedload(ServerModel.loader),
                selectinload(ServerModel.attributes)
            ).where(
                ServerModel.id == server_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            entity = self.servers_mapper.model_to_entity(
                model=record
            )

            stmt = delete(
                ServerModel
            ).where(
                ServerModel.id == server_id
            )

            await session.execute(stmt)

            if not session_provided:
                await session.commit()

            return entity

    async def delete_many(
        self,
        server_ids: List[int],
        session: Optional[AsyncSession] = None
    ) -> List[ServerEntity]:
        """
        Deletes multiple existing servers.

        Parameters:
        - server_ids: List of server IDs.
        - session: AsyncSession object.

        Returns:
        - List: List of ServerEntity objects.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                ServerModel
            ).options(
                joinedload(ServerModel.game).selectinload(GameModel.loaders),
                joinedload(ServerModel.loader),
                selectinload(ServerModel.attributes)
            ).where(
                ServerModel.id.in_(server_ids)
            )

            result = await session.execute(stmt)
            records = cast(List[ServerModel], result.scalars().all())

            entities = self.servers_mapper.models_to_entities(
                models=records
            )

            stmt = delete(
                ServerModel
            ).where(
                ServerModel.id.in_(server_ids)
            )

            await session.execute(stmt)

            if not session_provided:
                await session.commit()

            return entities