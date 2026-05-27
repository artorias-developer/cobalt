#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, cast, List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from domain.exceptions import (
    UnexpectedError,
    ConflictError
)
from domain.entities import (
    RoleEntity,
    RolesPageEntity,
    RolesGetPageEntity,
    RoleCreateEntity,
    RoleUpdateEntity
)
from domain.repositories import AbstractRolesRepository
from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.databases.mappers import AbstractRolesRepositoryMapper
from infrastructure.databases.postgres.models import RoleModel
from infrastructure.databases.postgres.repositories import BaseRepository
from infrastructure.databases.shared import (
    IntegrityCodesEnum,
    RepositoryOperationsEnum
)


class RolesRepository(AbstractRolesRepository, BaseRepository):
    """
    Repository for working with the 'users_roles' table.
    """
    roles_mapper: AbstractRolesRepositoryMapper
    logger: AbstractLogger

    def __init__(
        self,
        async_session: async_sessionmaker,
        roles_mapper: AbstractRolesRepositoryMapper,
        logger: AbstractLogger
    ):
        super().__init__(async_session)

        self.roles_mapper = roles_mapper
        self.logger = logger

    def _handle_integrity_error(
        self,
        e: IntegrityError,
        operation: RepositoryOperationsEnum
    ) -> None:
        """
        Handles IntegrityError exceptions for role operations.

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
                role_name = details.get("name")

                raise ConflictError(f'Role "{role_name}" already exists') from e

        if sqlstate == IntegrityCodesEnum.FOREIGN_KEY_VIOLATION:
            if operation == RepositoryOperationsEnum.DELETE:
                role_id = details.get("id")

                raise ConflictError(f"Role {role_id} is still assigned to users") from e

        self.logger.exception(f"Unhandled DB integrity error during {operation}:")
        raise UnexpectedError("Internal server error") from e

    async def get_page(
        self,
        entity: RolesGetPageEntity,
        session: Optional[AsyncSession] = None
    ) -> RolesPageEntity:
        """
        Gets a paginated list of roles.

        Parameters:
        - entity: RolesGetPageEntity object.
        - session: AsyncSession object.

        Returns:
        - RolesPageEntity: RolesPageEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(RoleModel)

            if entity.search:
                stmt = stmt.filter(RoleModel.name.ilike(f"%{entity.search}%"))

            if entity.sort_field:
                sort_col = getattr(RoleModel, entity.sort_field)

                stmt = stmt.order_by(
                    sort_col.desc() if entity.sort_direction == "desc" else sort_col.asc()
                )

            records, total, page, pages = await self.paginate(
                session=session,
                stmt=stmt,
                page=entity.page,
                limit=entity.limit
            )

            records = cast(List[RoleModel], records)

            roles = self.roles_mapper.models_to_entities(
                models=records
            )

            return RolesPageEntity(
                roles=roles,
                total=total,
                page=page,
                pages=pages
            )

    async def get_one_by_id(
        self,
        role_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[RoleEntity]:
        """
        Gets an existing role by ID.

        Parameters:
        - role_id: Role ID.
        - session: AsyncSession object.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                RoleModel
            ).filter(
                RoleModel.id == role_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            return self.roles_mapper.model_to_entity(
                model=record
            )

    async def create_one(
        self,
        entity: RoleCreateEntity,
        session: Optional[AsyncSession] = None
    ) -> RoleEntity:
        """
        Creates a new role.

        Parameters:
        - entity: RoleCreateEntity object.
        - session: AsyncSession object.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            record = self.roles_mapper.create_entity_to_model(
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

            return self.roles_mapper.model_to_entity(
                model=record
            )

    async def update_one(
        self,
        entity: RoleUpdateEntity,
        session: Optional[AsyncSession] = None
    ) -> Optional[RoleEntity]:
        """
        Updates an existing role.

        Parameters:
        - entity: RoleUpdateEntity object.
        - session: AsyncSession object.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                RoleModel
            ).filter(
                RoleModel.id == entity.id
            )

            try:
                result = await session.execute(stmt)
                record = result.scalars().first()

                if not record:
                    return None

                record = self.roles_mapper.update_entity_to_model(
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

            return self.roles_mapper.model_to_entity(
                model=record
            )

    async def delete_one(
        self,
        role_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[RoleEntity]:
        """
        Deletes an existing role.

        Parameters:
        - role_id: Role ID.
        - session: AsyncSession object.

        Returns:
        - RoleEntity: RoleEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = delete(
                RoleModel
            ).where(
                RoleModel.id == role_id
            ).returning(
                RoleModel
            )

            try:
                result = await session.execute(stmt)
                record = result.scalars().first()

                if not record:
                    return None

                if session_provided:
                    await session.flush()
                else:
                    await session.commit()

            except IntegrityError as e:
                if not session_provided:
                    await session.rollback()

                self._handle_integrity_error(
                    e=e,
                    operation=RepositoryOperationsEnum.DELETE
                )

            return self.roles_mapper.model_to_entity(
                model=record
            )

    async def delete_many(
        self,
        role_ids: List[int],
        session: Optional[AsyncSession] = None
    ) -> List[RoleEntity]:
        """
        Deletes multiple existing roles.

        Parameters:
        - role_ids: List of role IDs.
        - session: AsyncSession object.

        Returns:
        - List: List of RoleEntity objects.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = delete(
                RoleModel
            ).where(
                RoleModel.id.in_(role_ids)
            ).returning(
                RoleModel
            )

            try:
                result = await session.execute(stmt)
                records = cast(List[RoleModel], result.scalars().all())

                if session_provided:
                    await session.flush()
                else:
                    await session.commit()

            except IntegrityError as e:
                if not session_provided:
                    await session.rollback()

                self._handle_integrity_error(
                    e=e,
                    operation=RepositoryOperationsEnum.DELETE
                )

            return self.roles_mapper.models_to_entities(
                models=records
            )