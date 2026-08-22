#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from secrets import token_urlsafe
from typing import Optional

from domain.exceptions import (
    ConflictError,
    AuthenticationError,
    NotFoundError,
    ValidationError
)
from domain.value_objects import Password, Login
from application.contracts.clients import AbstractCacheClient
from application.contracts.services import (
    AbstractUsersService,
    AbstractAuthService
)
from application.contracts.hashers import AbstractHasher
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    UserDto,
    UserUpdateDto,
    AuthLoginDto,
    AuthSessionDto,
    AuthChangeCredentialsDto
)


class AuthService(AbstractAuthService):
    """
    Auth service for session-based authentication using Redis.
    """
    cache_client: AbstractCacheClient
    users_service: AbstractUsersService
    hasher: AbstractHasher

    def __init__(
        self,
        cache_client: AbstractCacheClient,
        users_service: AbstractUsersService,
        hasher: AbstractHasher
    ):
        self.cache_client = cache_client
        self.users_service = users_service
        self.hasher = hasher

    async def login(
        self,
        dto: AuthLoginDto,
        old_session_id: Optional[str] = None
    ) -> AuthSessionDto:
        """
        Authenticates user and creates session.

        Parameters:
        - dto: AuthLoginDto object.
        - old_session_id: Old session ID.

        Returns:
        - AuthSessionDto: AuthSessionDto object.
        """
        login = Login(dto.login)
        password = Password(dto.password)

        received_dto = await self.users_service.get_one_by_login(
            login=login.value
        )

        if not received_dto:
            raise AuthenticationError("Invalid login or password")

        if not self.hasher.verify(
            plain=password.value,
            hashed=received_dto.hashed_password,
            salt=received_dto.salt
        ):
            raise AuthenticationError("Invalid login or password")

        if old_session_id:
            old_key = self.cache_client.format_pattern(
                pattern=CacheConstants.SESSION_KEY,
                session_id=old_session_id
            )

            await self.cache_client.delete(
                keys=old_key
            )

        session_id = token_urlsafe(32)

        key = self.cache_client.format_pattern(
            pattern=CacheConstants.SESSION_KEY,
            session_id=session_id
        )

        await self.cache_client.set(
            key=key,
            value=str(received_dto.id),
            expire=CacheConstants.TTL_1_DAY,
            raise_on_error=True
        )

        return AuthSessionDto(
            session_id=session_id
        )

    async def logout(
        self,
        session_id: str
    ) -> None:
        """
        Deletes user session.

        Parameters:
        - session_id: Session id.

        Returns:
        - None.
        """
        key = self.cache_client.format_pattern(
            pattern=CacheConstants.SESSION_KEY,
            session_id=session_id
        )

        await self.cache_client.delete(
            keys=key
        )

    async def change_credentials(
        self,
        user_id: int,
        dto: AuthChangeCredentialsDto
    ) -> None:
        """
        Changes user login and/or password.

        Parameters:
        - user_id: User ID.
        - dto: AuthChangeCredentialsDto object.

        Returns:
        - None.
        """
        received_dto = await self.users_service.get_one_by_id(
            user_id=user_id
        )

        if not received_dto:
            raise NotFoundError("User not found")

        if dto.new_password:
            if not dto.old_password:
                raise ValidationError("Current password is required")

            old_password = Password(dto.old_password)

            is_valid = self.hasher.verify(
                plain=old_password.value,
                hashed=received_dto.hashed_password,
                salt=received_dto.salt
            )

            if not is_valid:
                raise ConflictError("Invalid current password")

        user_update_dto = UserUpdateDto(
            login=dto.login,
            password=dto.new_password
        )

        await self.users_service.update_one(
            user_id=user_id,
            dto=user_update_dto
        )

    async def get_session_user(
        self,
        session_id: str
    ) -> Optional[UserDto]:
        """
        Gets session by ID.

        Parameters:
        - session_id: Session ID.

        Returns:
        - UserDto: UserDto object.
        """
        key = self.cache_client.format_pattern(
            pattern=CacheConstants.SESSION_KEY,
            session_id=session_id
        )

        cached = await self.cache_client.get(
            key=key,
            raise_on_error=True
        )

        if cached:
            await self.cache_client.expire(
                key=key,
                seconds=CacheConstants.TTL_1_DAY
            )

            received_entity = await self.users_service.get_one_by_id(
                user_id=int(cached)
            )

            return received_entity

        return None
