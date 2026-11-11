#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest

from domain.exceptions import (
    AuthenticationError,
    ConflictError,
    ValidationError
)
from application.services import AuthService
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    AuthLoginDto,
    AuthSessionDto,
    AuthUpdateCredentialsDto,
    UserUpdateDto
)

from helpers.factories import make_user_dto


@pytest.fixture
def service(cache_client, users_service_mock, hasher) -> AuthService:
    return AuthService(
        cache_client=cache_client,
        users_service=users_service_mock,
        hasher=hasher
    )


class TestLogin:
    async def test_creates_session_for_valid_credentials(self, service, cache_client, users_service_mock, hasher):
        users_service_mock.get_one_by_login.return_value = make_user_dto(user_id=5)

        result = await service.login(AuthLoginDto(login="john_doe", password="Secret123"))

        assert isinstance(result, AuthSessionDto)
        assert len(result.session_id) >= 32
        hasher.verify.assert_called_once_with(plain="Secret123", hashed="hashed", salt="salt")
        cache_client.set.assert_awaited_once_with(
            key=f"session:{result.session_id}",
            value="5",
            expire=CacheConstants.TTL_1_DAY,
            raise_on_error=True
        )
        cache_client.delete.assert_not_awaited()

    async def test_generates_unique_session_ids(self, service, users_service_mock):
        users_service_mock.get_one_by_login.return_value = make_user_dto()
        dto = AuthLoginDto(login="john_doe", password="Secret123")

        first = await service.login(dto)
        second = await service.login(dto)

        assert first.session_id != second.session_id

    async def test_drops_previous_session(self, service, cache_client, users_service_mock):
        users_service_mock.get_one_by_login.return_value = make_user_dto()

        await service.login(AuthLoginDto(login="john_doe", password="Secret123"), old_session_id="old")

        cache_client.delete.assert_awaited_once_with(keys="session:old")

    async def test_wrong_password_raises_and_creates_no_session(self, service, cache_client, users_service_mock, hasher):
        users_service_mock.get_one_by_login.return_value = make_user_dto()
        hasher.verify.return_value = False

        with pytest.raises(AuthenticationError):
            await service.login(AuthLoginDto(login="john_doe", password="wrong_pass"))

        cache_client.set.assert_not_awaited()

    async def test_unknown_user_propagates_authentication_error(self, service, users_service_mock):
        users_service_mock.get_one_by_login.side_effect = AuthenticationError("Invalid login or password")

        with pytest.raises(AuthenticationError):
            await service.login(AuthLoginDto(login="ghost", password="Secret123"))

    @pytest.mark.parametrize(
        ("login", "password"),
        [("", "Secret123"), ("bad<login>", "Secret123"), ("john_doe", "ab")]
    )
    async def test_invalid_input_fails_before_lookup(self, service, users_service_mock, login, password):
        with pytest.raises(ValidationError):
            await service.login(AuthLoginDto(login=login, password=password))

        users_service_mock.get_one_by_login.assert_not_awaited()


class TestLogout:
    async def test_deletes_session_key(self, service, cache_client):
        await service.logout("abc")

        cache_client.delete.assert_awaited_once_with(keys="session:abc")


class TestGetSessionUser:
    async def test_returns_user_and_extends_ttl(self, service, cache_client, users_service_mock):
        user = make_user_dto(user_id=8)
        cache_client.get.return_value = "8"
        users_service_mock.get_one_by_id.return_value = user

        result = await service.get_session_user("abc")

        assert result == user
        cache_client.get.assert_awaited_once_with(key="session:abc", raise_on_error=True)
        cache_client.expire.assert_awaited_once_with(key="session:abc", seconds=CacheConstants.TTL_1_DAY)
        users_service_mock.get_one_by_id.assert_awaited_once_with(user_id=8)

    async def test_returns_none_for_unknown_session(self, service, cache_client, users_service_mock):
        cache_client.get.return_value = None

        assert await service.get_session_user("missing") is None

        cache_client.expire.assert_not_awaited()
        users_service_mock.get_one_by_id.assert_not_awaited()


class TestUpdateCredentials:
    async def test_updates_login_only(self, service, users_service_mock, hasher):
        users_service_mock.get_one_by_id.return_value = make_user_dto(user_id=1)

        await service.update_credentials(1, AuthUpdateCredentialsDto(login="new_login"))

        hasher.verify.assert_not_called()
        users_service_mock.update_one.assert_awaited_once_with(
            user_id=1,
            dto=UserUpdateDto(login="new_login", password=None)
        )

    async def test_updates_password_when_old_one_matches(self, service, users_service_mock, hasher):
        users_service_mock.get_one_by_id.return_value = make_user_dto(user_id=1)

        await service.update_credentials(
            1, AuthUpdateCredentialsDto(old_password="OldPass1", new_password="NewPass1")
        )

        hasher.verify.assert_called_once_with(plain="OldPass1", hashed="hashed", salt="salt")
        users_service_mock.update_one.assert_awaited_once_with(
            user_id=1,
            dto=UserUpdateDto(login=None, password="NewPass1")
        )

    async def test_requires_old_password(self, service, users_service_mock):
        users_service_mock.get_one_by_id.return_value = make_user_dto()

        with pytest.raises(ValidationError):
            await service.update_credentials(1, AuthUpdateCredentialsDto(new_password="NewPass1"))

        users_service_mock.update_one.assert_not_awaited()

    async def test_rejects_wrong_old_password(self, service, users_service_mock, hasher):
        users_service_mock.get_one_by_id.return_value = make_user_dto()
        hasher.verify.return_value = False

        with pytest.raises(ConflictError):
            await service.update_credentials(
                1, AuthUpdateCredentialsDto(old_password="WrongPass", new_password="NewPass1")
            )

        users_service_mock.update_one.assert_not_awaited()
