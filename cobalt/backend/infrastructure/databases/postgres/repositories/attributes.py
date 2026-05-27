#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, List, cast

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from domain.exceptions import (
    NotFoundError,
    ConflictError,
    UnexpectedError
)
from domain.entities import (
    AttributeEntity,
    AttributesPageEntity,
    AttributesGetPageEntity,
    AttributeCreateEntity,
    AttributeUpdateEntity
)
from domain.repositories import AbstractAttributesRepository
from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.databases.mappers import AbstractAttributesRepositoryMapper
from infrastructure.databases.postgres.models import AttributeModel
from infrastructure.databases.postgres.repositories import BaseRepository
from infrastructure.databases.shared import (
    IntegrityCodesEnum,
    RepositoryOperationsEnum
)


class AttributesRepository(AbstractAttributesRepository, BaseRepository):
    """
    Repository for working with the 'servers_attributes' table.
    """
    attributes_mapper: AbstractAttributesRepositoryMapper
    logger: AbstractLogger

    def __init__(
        self,
        async_session: async_sessionmaker,
        attributes_mapper: AbstractAttributesRepositoryMapper,
        logger: AbstractLogger
    ):
        super().__init__(async_session)

        self.attributes_mapper = attributes_mapper
        self.logger = logger

    def _handle_integrity_error(
        self,
        e: IntegrityError,
        operation: RepositoryOperationsEnum
    ) -> None:
        """
        Handles IntegrityError exceptions for attribute operations.

        Parameters:
        - e: The IntegrityError exception.
        - operation: The operation that caused the error.

        Returns:
        - None.
        """
        sqlstate = getattr(e.orig, "sqlstate", None)
        details = self.parse_asyncpg_detail_to_dict(e)

        if sqlstate == IntegrityCodesEnum.FOREIGN_KEY_VIOLATION:
            if operation == RepositoryOperationsEnum.CREATE:
                server_id = details.get("server_id")

                raise NotFoundError(f"Server {server_id} not found") from e

        if sqlstate == IntegrityCodesEnum.UNIQUE_VIOLATION:
            if operation in [
                RepositoryOperationsEnum.CREATE,
                RepositoryOperationsEnum.UPDATE
            ]:
                key = details.get("key")
                server_id = details.get("server_id")

                raise ConflictError(f'Attribute "{key}" already exists for server {server_id}') from e

        self.logger.exception(f"Unhandled DB integrity error during {operation}:")
        raise UnexpectedError("Internal server error") from e

    async def get_page(
        self,
        server_id: int,
        entity: AttributesGetPageEntity,
        session: Optional[AsyncSession] = None
    ) -> AttributesPageEntity:
        """
        Gets a paginated list of attributes.

        Parameters:
        - server_id: Server ID.
        - entity: AttributesGetPageEntity object.
        - session: AsyncSession object.

        Returns:
        - AttributesPageEntity: AttributesPageEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                AttributeModel
            ).filter(
                AttributeModel.server_id == server_id
            )

            if entity.search:
                stmt = stmt.filter(
                    AttributeModel.key.ilike(f"%{entity.search}%") |
                    AttributeModel.value.ilike(f"%{entity.search}%")
                )

            if entity.sort_field:
                sort_col = getattr(AttributeModel, entity.sort_field)

                stmt = stmt.order_by(
                    sort_col.desc() if entity.sort_direction == "desc" else sort_col.asc()
                )

            records, total, page, pages = await self.paginate(
                session=session,
                stmt=stmt,
                page=entity.page,
                limit=entity.limit
            )

            records = cast(List[AttributeModel], records)

            attributes = self.attributes_mapper.models_to_entities(
                models=records
            )

            return AttributesPageEntity(
                attributes=attributes,
                total=total,
                page=page,
                pages=pages
            )

    async def get_one_by_id(
        self,
        attribute_id: int,
        server_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[AttributeEntity]:
        """
        Gets an existing attribute.

        Parameters:
        - attribute_id: Attribute ID.
        - server_id: Server Attribute ID.
        - session: AsyncSession object.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                AttributeModel
            ).filter(
                AttributeModel.id == attribute_id,
                AttributeModel.server_id == server_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            return self.attributes_mapper.model_to_entity(
                model=record
            )

    async def create_one(
        self,
        server_id: int,
        entity: AttributeCreateEntity,
        session: Optional[AsyncSession] = None
    ) -> AttributeEntity:
        """
        Creates the new attributes.

        Parameters:
        - server_id: Server ID.
        - entity: AttributeCreateEntity object.
        - session: AsyncSession object.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            record = self.attributes_mapper.create_entity_to_model(
                server_id=server_id,
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

            return self.attributes_mapper.model_to_entity(
                model=record
            )

    async def create_many(
        self,
        server_id: int,
        entities: List[AttributeCreateEntity],
        session: Optional[AsyncSession] = None
    ) -> List[AttributeEntity]:
        """
        Creates the new attributes.

        Parameters:
        - server_id: Server ID.
        - entities: List of AttributeCreateEntity objects.
        - session: AsyncSession object.

        Returns:
        - List: List of AttributeEntity objects.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            records = self.attributes_mapper.create_entities_to_models(
                server_id=server_id,
                entities=entities
            )

            try:
                session.add_all(records)

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

            return self.attributes_mapper.models_to_entities(
                models=records
            )

    async def update_one(
        self,
        server_id: int,
        entity: AttributeUpdateEntity,
        session: Optional[AsyncSession] = None
    ) -> Optional[AttributeEntity]:
        """
        Updates an existing attribute.

        Parameters:
        - server_id: Server ID.
        - entity: AttributeUpdateEntity object.
        - session: AsyncSession object.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                AttributeModel
            ).filter(
                AttributeModel.id == entity.id,
                AttributeModel.server_id == server_id
            )

            try:
                result = await session.execute(stmt)
                record = result.scalars().first()

                if not record:
                    return None

                record = self.attributes_mapper.update_entity_to_model(
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

            return self.attributes_mapper.model_to_entity(
                model=record
            )

    async def update_many(
        self,
        server_id: int,
        entities: List[AttributeUpdateEntity],
        session: Optional[AsyncSession] = None
    ) -> List[AttributeEntity]:
        """
        Updates existing attributes.

        Parameters:
        - server_id: Server ID.
        - entities: List of AttributeUpdateEntity objects.
        - session: AsyncSession object.

        Returns:
        - List: List of AttributeEntity objects.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            attribute_ids = [
                attr.id
                for attr in entities
            ]

            stmt = select(
                AttributeModel
            ).filter(
                AttributeModel.id.in_(attribute_ids),
                AttributeModel.server_id == server_id
            )


            try:
                result = await session.execute(stmt)
                records = cast(List[AttributeModel], result.scalars().all())

                records = self.attributes_mapper.update_entities_to_models(
                    models=records,
                    entities=entities
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

            return self.attributes_mapper.models_to_entities(
                models=records
            )

    async def delete_one(
        self,
        server_id: int,
        attribute_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[AttributeEntity]:
        """
        Deletes an existing attributes.

        Parameters:
        - server_id: Server ID.
        - attribute_id: Attribute ID.
        - session: AsyncSession object.

        Returns:
        - AttributeEntity: AttributeEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = delete(
                AttributeModel
            ).where(
                AttributeModel.id == attribute_id,
                AttributeModel.server_id == server_id
            ).returning(
                AttributeModel
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            if not session_provided:
                await session.commit()

            return self.attributes_mapper.model_to_entity(
                model=record
            )

    async def delete_many(
        self,
        server_id: int,
        attribute_ids: List[int],
        session: Optional[AsyncSession] = None
    ) -> List[AttributeEntity]:
        """
        Deletes existing attributes.

        Parameters:
        - server_id: Server ID.
        - attribute_ids: List of attribute IDs.
        - session: AsyncSession object.

        Returns:
        - List: List of AttributeEntity objects.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = delete(
                AttributeModel
            ).where(
                AttributeModel.id.in_(attribute_ids),
                AttributeModel.server_id == server_id
            ).returning(
                AttributeModel
            )

            result = await session.execute(stmt)
            records = cast(List[AttributeModel], result.scalars().all())

            if not session_provided:
                await session.commit()

            return self.attributes_mapper.models_to_entities(
                models=records
            )