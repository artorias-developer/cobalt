#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Tuple

from orjson import loads

from domain.exceptions import (
    NotFoundError,
    AuthenticationError
)
from domain.value_objects import Password
from domain.repositories import AbstractUsersRepository
from application.contracts.clients import AbstractCacheClient
from application.contracts.services import (
    AbstractUsersService,
    AbstractRolesService,
    AbstractSettingsService
)
from application.contracts.hashers import AbstractHasher
from application.contracts.mappers import AbstractUsersServiceMapper
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    UserDto,
    UsersGetPageDto,
    UsersPageDto,
    UserCreateDto,
    UserUpdateDto
)


class UsersService(AbstractUsersService):
    """
    Users service.
    """
    cache_client: AbstractCacheClient
    users_repository: AbstractUsersRepository
    users_mapper: AbstractUsersServiceMapper
    hasher: AbstractHasher
    roles_service: AbstractRolesService
    settings_service: AbstractSettingsService

    def __init__(
        self,
        cache_client: AbstractCacheClient,
        users_repository: AbstractUsersRepository,
        users_mapper: AbstractUsersServiceMapper,
        hasher: AbstractHasher,
        roles_service: AbstractRolesService,
        settings_service: AbstractSettingsService
    ):
        self.cache_client = cache_client
        self.users_repository = users_repository
        self.users_mapper = users_mapper
        self.hasher = hasher
        self.roles_service = roles_service
        self.settings_service = settings_service

    def _hash_password(
        self,
        password: str
    ) -> Tuple[str, str]:
        """
        Generates a salt and hashes the given password.

        Parameters:
        - password: Password to hash.

        Returns:
        - Tuple: Hashed password and local salt.
        """
        salt = self.hasher.generate_salt(
            length=32
        )

        hashed_password = self.hasher.hash(
            plain=password,
            salt=salt
        )

        return hashed_password, salt

    async def get_page(
        self,
        dto: UsersGetPageDto
    ) -> UsersPageDto:
        """
        Gets a paginated list of users.

        Parameters:
        - dto: UsersGetPageDto object.

        Returns:
        - UsersPageDto: UsersPageDto object.
        """
        key = self.cache_client.format_pattern(
            pattern=CacheConstants.USERS_PAGE_KEY,
            page=dto.page,
            search=dto.search,
            sort_field=dto.sort_field,
            sort_direction=dto.sort_direction,
            limit=dto.limit
        )

        cached = await self.cache_client.get(
            key=key
        )

        if cached:
            data = loads(cached)
            return UsersPageDto.from_dict(data)

        mapped_entity = self.users_mapper.get_page_dto_to_entity(
            dto=dto
        )

        received_entity = await self.users_repository.get_page(
            entity=mapped_entity
        )

        if not received_entity.users:
            raise NotFoundError("Users not found")

        mapped_dto = self.users_mapper.page_entity_to_dto(
            entity=received_entity
        )

        await self.cache_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.TTL_1_HOUR
        )

        return mapped_dto

    async def get_one_by_id(
        self,
        user_id: int
    ) -> UserDto:
        """
        Gets an existing user by ID.

        Parameters:
        - user_id: User ID.

        Returns:
        - UserDto: UserDto object.
        """
        search_key = self.cache_client.format_pattern(
            pattern=CacheConstants.USERS_ITEM_KEY,
            user_id=user_id
        )

        cached = await self.cache_client.get(
            pattern=search_key
        )

        if cached:
            data = loads(cached)
            return UserDto.from_dict(data)

        received_entity = await self.users_repository.get_one_by_id(
            user_id=user_id
        )

        if not received_entity:
            raise NotFoundError("User {user_id} not found", user_id=user_id)

        key = self.cache_client.format_pattern(
            pattern=CacheConstants.USERS_ITEM_KEY,
            user_id=received_entity.id,
            login=received_entity.login.value,
            role_id=received_entity.role.id
        )

        mapped_dto = self.users_mapper.entity_to_dto(
            entity=received_entity
        )

        await self.cache_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.TTL_1_HOUR
        )

        return mapped_dto

    async def get_one_by_login(
        self,
        login: str
    ) -> UserDto:
        """
        Gets an existing user by login.

        Parameters:
        - login: User login.

        Returns:
        - UserDto: UserDto object.
        """
        search_key = self.cache_client.format_pattern(
            pattern=CacheConstants.USERS_ITEM_KEY,
            login=login
        )

        cached = await self.cache_client.get(
            pattern=search_key
        )

        if cached:
            data = loads(cached)
            return UserDto.from_dict(data)

        received_entity = await self.users_repository.get_one_by_login(
            login=login
        )

        if not received_entity:
            raise AuthenticationError("Invalid login or password")

        key = self.cache_client.format_pattern(
            pattern=CacheConstants.USERS_ITEM_KEY,
            user_id=received_entity.id,
            login=received_entity.login.value,
            role_id=received_entity.role.id
        )

        mapped_dto = self.users_mapper.entity_to_dto(
            entity=received_entity
        )

        await self.cache_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.TTL_1_HOUR
        )

        return mapped_dto

    async def create_one(
        self,
        dto: UserCreateDto
    ) -> UserDto:
        """
        Creates a new user.

        Parameters:
        - dto: UserCreateDto object.

        Returns:
        - UserDto: UserDto object.
        """
        password = Password(dto.password)

        hashed_password, local_salt = self._hash_password(
            password=password.value
        )

        mapped_entity = self.users_mapper.create_dto_to_entity(
            dto=dto,
            hashed_password=hashed_password,
            salt=local_salt
        )

        created_entity = await self.users_repository.create_one(
            entity=mapped_entity
        )

        await self.cache_client.delete(
            patterns=self.cache_client.format_pattern(
                pattern=CacheConstants.USERS_PAGE_KEY
            )
        )

        return self.users_mapper.entity_to_dto(
            entity=created_entity
        )

    async def update_one(
        self,
        user_id: int,
        dto: UserUpdateDto
    ) -> UserDto:
        """
        Updates an existing user.

        Parameters:
        - user_id: User ID.
        - dto: UserUpdateDto object.

        Returns:
        - UserDto: UserDto object.
        """
        if dto.password is not None:
            password = Password(dto.password)

            hashed_password, local_salt = self._hash_password(
                password=password.value
            )
        else:
            hashed_password = None
            local_salt = None

        mapped_entity = self.users_mapper.update_dto_to_entity(
            user_id=user_id,
            dto=dto,
            hashed_password=hashed_password,
            salt=local_salt
        )

        updated_entity = await self.users_repository.update_one(
            entity=mapped_entity
        )

        if not updated_entity:
            raise NotFoundError("User {user_id} not found", user_id=user_id)

        await self.cache_client.delete(
            patterns=[
                self.cache_client.format_pattern(
                    pattern=CacheConstants.USERS_ITEM_KEY,
                    user_id=user_id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.USERS_PAGE_KEY
                )
            ]
        )

        return self.users_mapper.entity_to_dto(
            entity=updated_entity
        )

    async def delete_one(
        self,
        user_id: int
    ) -> None:
        """
        Deletes an existing user.

        Parameters:
        - user_id: User ID.

        Returns:
        - None.
        """
        deleted_entity = await self.users_repository.delete_one(
            user_id=user_id
        )

        if not deleted_entity:
            raise NotFoundError("User {user_id} not found", user_id=user_id)

        await self.cache_client.delete(
            patterns=[
                self.cache_client.format_pattern(
                    pattern=CacheConstants.USERS_ITEM_KEY,
                    user_id=user_id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.USERS_PAGE_KEY
                )
            ]
        )

    async def delete_many(
        self,
        user_ids: List[int]
    ) -> None:
        """
        Deletes multiple existing users.

        Parameters:
        - user_ids: List of user IDs.

        Returns:
        - None.
        """
        deleted_entities = await self.users_repository.delete_many(
            user_ids=user_ids
        )

        if not deleted_entities:
            raise NotFoundError("Users not found")

        patterns_to_delete = [
            self.cache_client.format_pattern(
                pattern=CacheConstants.USERS_PAGE_KEY
            )
        ]

        for entity in deleted_entities:
            patterns_to_delete.append(
                self.cache_client.format_pattern(
                    pattern=CacheConstants.USERS_ITEM_KEY,
                    user_id=entity.id
                )
            )

        await self.cache_client.delete(
            patterns=patterns_to_delete
        )