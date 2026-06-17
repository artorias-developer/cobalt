#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from secrets import token_urlsafe
from typing import Optional, Callable

from domain.exceptions import (
    ConflictError,
    AuthenticationError,
    NotFoundError,
    ValidationError
)
from application.contracts.managers import AbstractI18nManager
from application.contracts.clients import AbstractCachesClient
from application.contracts.services import (
    AbstractPasswordsService,
    AbstractUsersService,
    AbstractAuthService
)
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
    caches_client: AbstractCachesClient
    users_service: AbstractUsersService
    passwords_service: AbstractPasswordsService
    i18n_manager: AbstractI18nManager

    _: Callable

    def __init__(
        self,
        caches_client: AbstractCachesClient,
        users_service: AbstractUsersService,
        passwords_service: AbstractPasswordsService,
        i18n_manager: AbstractI18nManager
    ):
        self.caches_client = caches_client
        self.users_service = users_service
        self.passwords_service = passwords_service
        self.i18n_manager = i18n_manager

        self._ = i18n_manager.gettext

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
        received_entity = await self.users_service.get_one_by_login(
            login=dto.login
        )

        if not received_entity:
            raise AuthenticationError(self._("Invalid login or password"))

        if not self.passwords_service.verify_password(
            plain_password=dto.password,
            hashed_password=received_entity.hashed_password,
            local_salt=received_entity.salt
        ):
            raise AuthenticationError(self._("Invalid login or password"))

        if old_session_id:
            old_key = self.caches_client.format_pattern(
                pattern=CacheConstants.SESSION_KEY,
                session_id=old_session_id
            )

            await self.caches_client.delete(
                keys=old_key
            )

        session_id = token_urlsafe(32)

        key = self.caches_client.format_pattern(
            pattern=CacheConstants.SESSION_KEY,
            session_id=session_id
        )

        await self.caches_client.set(
            key=key,
            value=str(received_entity.id),
            expire=CacheConstants.LONG_TTL_SECONDS,
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
        key = self.caches_client.format_pattern(
            pattern=CacheConstants.SESSION_KEY,
            session_id=session_id
        )

        await self.caches_client.delete(
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
        received_entity = await self.users_service.get_one_by_id(
            user_id=user_id
        )

        if not received_entity:
            raise NotFoundError(self._("User not found"))

        if dto.new_password:
            if not dto.old_password:
                raise ValidationError(self._("Current password is required"))

            is_valid = self.passwords_service.verify_password(
                plain_password=dto.old_password,
                hashed_password=received_entity.hashed_password,
                local_salt=received_entity.salt
            )

            if not is_valid:
                raise ConflictError(self._("Invalid current password"))

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
        key = self.caches_client.format_pattern(
            pattern=CacheConstants.SESSION_KEY,
            session_id=session_id
        )

        cached = await self.caches_client.get(
            key=key,
            raise_on_error=True
        )

        if cached:
            await self.caches_client.expire(
                key=key,
                seconds=CacheConstants.LONG_TTL_SECONDS
            )

            received_entity = await self.users_service.get_one_by_id(
                user_id=int(cached)
            )

            return received_entity

        return None
