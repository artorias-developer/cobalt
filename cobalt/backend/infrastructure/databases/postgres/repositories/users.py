#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, List, cast, Callable

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from domain.exceptions import (
    NotFoundError,
    ConflictError,
    UnexpectedError
)
from domain.entities import (
    UserEntity,
    UsersPageEntity,
    UsersGetPageEntity,
    UserCreateEntity,
    UserUpdateEntity
)
from domain.repositories import AbstractUsersRepository
from application.contracts.managers import AbstractI18nManager
from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.databases.mappers import AbstractUsersRepositoryMapper
from infrastructure.databases.postgres.models import (
    UserModel,
    RoleModel,
    SettingsModel
)
from infrastructure.databases.postgres.repositories import BaseRepository
from infrastructure.databases.shared import (
    IntegrityCodesEnum,
    RepositoryOperationsEnum
)


class UsersRepository(AbstractUsersRepository, BaseRepository):
    """
    Repository for working with the 'users' table.
    """
    users_mapper: AbstractUsersRepositoryMapper
    i18n_manager: AbstractI18nManager
    logger: AbstractLogger

    _: Callable

    def __init__(
        self,
        async_session: async_sessionmaker,
        users_mapper: AbstractUsersRepositoryMapper,
        i18n_manager: AbstractI18nManager,
        logger: AbstractLogger
    ):
        super().__init__(async_session)

        self.users_mapper = users_mapper
        self.i18n_manager = i18n_manager
        self.logger = logger

        self._ = i18n_manager.gettext

    def _handle_integrity_error(
        self,
        e: IntegrityError,
        operation: RepositoryOperationsEnum
    ) -> None:
        """
        Handles IntegrityError exceptions for user operations.

        Parameters:
        - e: The IntegrityError exception.
        - operation: The operation that caused the error.

        Returns:
        - None.
        """
        sqlstate = getattr(e.orig, "sqlstate", None)
        details = self.parse_asyncpg_detail_to_dict(e)

        if sqlstate == IntegrityCodesEnum.FOREIGN_KEY_VIOLATION:
            if operation in [
                RepositoryOperationsEnum.CREATE,
                RepositoryOperationsEnum.UPDATE
            ]:
                role_id = details.get("role_id")

                raise NotFoundError(self._("Role {role_id} not found").format(role_id=role_id)) from e

        if sqlstate == IntegrityCodesEnum.UNIQUE_VIOLATION:
            if operation in [
                RepositoryOperationsEnum.CREATE,
                RepositoryOperationsEnum.UPDATE
            ]:
                user_login = details.get("login")

                raise ConflictError(self._('User "{user_login}" already exists').format(user_login=user_login)) from e

        self.logger.exception(f"Unhandled DB integrity error during {operation}:")
        raise UnexpectedError(self._("Internal server error")) from e

    async def get_page(
        self,
        entity: UsersGetPageEntity,
        session: Optional[AsyncSession] = None
    ) -> UsersPageEntity:
        """
        Gets a paginated list of users.

        Parameters:
        - entity: UsersGetPageEntity object.
        - session: AsyncSession object.

        Returns:
        - UsersPageEntity: UsersPageEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                UserModel
            ).options(
                joinedload(UserModel.role),
                joinedload(UserModel.settings)
            )

            if entity.search:
                stmt = stmt.filter(
                    UserModel.login.ilike(f"%{entity.search}%") |
                    UserModel.role.has(
                        RoleModel.name.ilike(f"%{entity.search}%")
                    )
                )

            if entity.sort_field:
                sort_col = getattr(UserModel, entity.sort_field)

                stmt = stmt.order_by(
                    sort_col.desc() if entity.sort_direction == "desc" else sort_col.asc()
                )

            records, total, page, pages = await self.paginate(
                session=session,
                stmt=stmt,
                page=entity.page,
                limit=entity.limit
            )

            records = cast(List[UserModel], records)

            users = self.users_mapper.models_to_entities(
                models=records
            )

            return UsersPageEntity(
                users=users,
                total=total,
                page=page,
                pages=pages
            )

    async def get_one_by_id(
        self,
        user_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[UserEntity]:
        """
        Gets an existing user by ID.

        Parameters:
        - user_id: User ID.
        - session: AsyncSession object.

        Returns:
        - UserEntity: UserEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                UserModel
            ).options(
                joinedload(UserModel.role),
                joinedload(UserModel.settings)
            ).filter(
                UserModel.id == user_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            return self.users_mapper.model_to_entity(
                model=record
            )

    async def get_one_by_login(
        self,
        login: str,
        session: Optional[AsyncSession] = None
    ) -> Optional[UserEntity]:
        """
        Gets an existing user by login.

        Parameters:
        - login: Login of the user.
        - session: AsyncSession object.

        Returns:
        - UserEntity: UserEntity object.
        """
        async with self._get_session(session) as session:
            stmt = select(
                UserModel
            ).options(
                joinedload(UserModel.role),
                joinedload(UserModel.settings)
            ).filter(
                UserModel.login == login
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            return self.users_mapper.model_to_entity(
                model=record
            )

    async def create_one(
        self,
        entity: UserCreateEntity,
        session: Optional[AsyncSession] = None
    ) -> UserEntity:
        """
        Creates a new user.

        Parameters:
        - entity: UserCreateEntity object.
        - session: AsyncSession object.

        Returns:
        - UserEntity: UserEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            user_record = self.users_mapper.create_entity_to_model(
                entity=entity
            )

            try:
                session.add(user_record)
                await session.flush()

                settings_record = SettingsModel(
                    user_id=user_record.id
                )

                session.add(settings_record)

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
                UserModel
            ).options(
                joinedload(UserModel.role),
                joinedload(UserModel.settings)
            ).filter(
                UserModel.id == user_record.id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            return self.users_mapper.model_to_entity(
                model=record
            )

    async def update_one(
        self,
        entity: UserUpdateEntity,
        session: Optional[AsyncSession] = None
    ) -> Optional[UserEntity]:
        """
        Updates an existing user.

        Parameters:
        - entity: UserUpdateEntity object.
        - session: AsyncSession object.

        Returns:
        - UserEntity: UserEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                UserModel
            ).options(
                joinedload(UserModel.role),
                joinedload(UserModel.settings)
            ).filter(
                UserModel.id == entity.id
            )

            try:
                result = await session.execute(stmt)
                record = result.scalars().first()

                if not record:
                    return None

                record = self.users_mapper.update_entity_to_model(
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

            return self.users_mapper.model_to_entity(
                model=record
            )

    async def delete_one(
        self,
        user_id: int,
        session: Optional[AsyncSession] = None
    ) -> Optional[UserEntity]:
        """
        Deletes an existing user.

        Parameters:
        - user_id: User ID.
        - session: AsyncSession object.

        Returns:
        - UserEntity: UserEntity object.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                UserModel
            ).options(
                joinedload(UserModel.role),
                joinedload(UserModel.settings)
            ).where(
                UserModel.id == user_id
            )

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                return None

            entity = self.users_mapper.model_to_entity(
                model=record
            )

            stmt = delete(
                UserModel
            ).where(
                UserModel.id == user_id
            )

            await session.execute(stmt)

            if not session_provided:
                await session.commit()

            return entity

    async def delete_many(
        self,
        user_ids: List[int],
        session: Optional[AsyncSession] = None
    ) -> List[UserEntity]:
        """
        Deletes multiple existing users.

        Parameters:
        - user_ids: List of user IDs.
        - session: AsyncSession object.

        Returns:
        - List: List of UserEntity objects.
        """
        session_provided = session is not None

        async with self._get_session(session) as session:
            stmt = select(
                UserModel
            ).options(
                joinedload(UserModel.role),
                joinedload(UserModel.settings)
            ).where(
                UserModel.id.in_(user_ids)
            )

            result = await session.execute(stmt)
            records = cast(List[UserModel], result.scalars().all())

            entities = self.users_mapper.models_to_entities(
                models=records
            )

            stmt = delete(
                UserModel
            ).where(
                UserModel.id.in_(user_ids)
            )

            await session.execute(stmt)

            if not session_provided:
                await session.commit()

            return entities