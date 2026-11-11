#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest

from domain.exceptions import (
    NotFoundError,
    AuthenticationError,
    ValidationError
)
from domain.value_objects import Batch, Login, HashedPassword, Salt
from domain.entities import UserCreateEntity, UserUpdateEntity
from application.mappers import (
    RolesServiceMapper,
    SettingsServiceMapper,
    UsersServiceMapper
)
from application.services import UsersService
from application.clients.caches.shared import CacheConstants
from application.managers.events.shared import RoleEventEnum
from application.dtos import (
    UsersPageDto,
    UsersGetPageDto,
    UserCreateDto,
    UserUpdateDto
)

from helpers.factories import (
    make_role_entity,
    make_role_dto,
    make_user_entity,
    make_users_page_entity,
    make_user_dto,
    make_connection
)


@pytest.fixture
def service(cache_client, users_repository, hasher, roles_service_mock, connections_manager) -> UsersService:
    return UsersService(
        cache_client=cache_client,
        users_repository=users_repository,
        users_mapper=UsersServiceMapper(
            roles_mapper=RolesServiceMapper(),
            settings_mapper=SettingsServiceMapper()
        ),
        hasher=hasher,
        roles_service=roles_service_mock,
        connections_manager=connections_manager
    )


class TestGetPage:
    async def test_returns_cached_page(self, service, cache_client, users_repository):
        cached = UsersPageDto(users=[make_user_dto()], total=1, page=1, pages=1)
        cache_client.get.return_value = cached.model_dump_json()

        result = await service.get_page(UsersGetPageDto(page=1))

        assert result == cached
        users_repository.get_page.assert_not_awaited()

    async def test_loads_from_repository_and_caches(self, service, cache_client, users_repository):
        users_repository.get_page.return_value = make_users_page_entity()

        result = await service.get_page(UsersGetPageDto(page=1))

        assert result.users[0].login == "john_doe"
        cache_client.set.assert_awaited_once()
        assert cache_client.set.await_args.kwargs["expire"] == CacheConstants.TTL_1_HOUR

    async def test_raises_not_found_on_empty_page(self, service, users_repository):
        users_repository.get_page.return_value = make_users_page_entity(users=[])

        with pytest.raises(NotFoundError):
            await service.get_page(UsersGetPageDto(page=1))


class TestGetOne:
    async def test_get_by_id_searches_cache_by_pattern(self, service, cache_client, users_repository):
        cached = make_user_dto(user_id=3)
        cache_client.get.return_value = cached.model_dump_json()

        result = await service.get_one_by_id(3)

        assert result == cached
        cache_client.get.assert_awaited_once_with(pattern="users:item:3:*:*")
        users_repository.get_one_by_id.assert_not_awaited()

    async def test_get_by_id_caches_with_full_key(self, service, cache_client, users_repository):
        users_repository.get_one_by_id.return_value = make_user_entity(
            user_id=3, login="alice", role=make_role_entity(role_id=2)
        )

        result = await service.get_one_by_id(3)

        assert result.login == "alice"
        assert cache_client.set.await_args.kwargs["key"] == "users:item:3:alice:2"

    async def test_get_by_id_raises_not_found(self, service, users_repository):
        users_repository.get_one_by_id.return_value = None

        with pytest.raises(NotFoundError):
            await service.get_one_by_id(3)

    async def test_get_by_login_raises_authentication_error_for_unknown_login(self, service, users_repository):
        # Don't reveal whether the login exists.
        users_repository.get_one_by_login.return_value = None

        with pytest.raises(AuthenticationError):
            await service.get_one_by_login("ghost")

    async def test_get_by_login_returns_user(self, service, cache_client, users_repository):
        users_repository.get_one_by_login.return_value = make_user_entity(login="alice")

        result = await service.get_one_by_login("alice")

        cache_client.get.assert_awaited_once_with(pattern="users:item:*:alice:*")
        users_repository.get_one_by_login.assert_awaited_once_with(login="alice")
        assert result.login == "alice"


class TestCreateOne:
    async def test_hashes_password_and_creates_user(self, service, hasher, cache_client, users_repository):
        users_repository.create_one.return_value = make_user_entity(user_id=9, login="bob")

        result = await service.create_one(UserCreateDto(login="bob", password="Secret123", role_id=2))

        hasher.generate_salt.assert_called_once_with(length=32)
        hasher.hash.assert_called_once_with(plain="Secret123", salt="generated_salt")
        users_repository.create_one.assert_awaited_once_with(
            entity=UserCreateEntity(
                login=Login("bob"),
                hashed_password=HashedPassword("generated_hash"),
                salt=Salt("generated_salt"),
                role_id=2
            )
        )
        cache_client.delete.assert_awaited_once_with(patterns="users:page:*:*:*:*:*")
        assert result.id == 9

    @pytest.mark.parametrize("password", ["ab", " leading", "trailing ", "x" * 65])
    async def test_rejects_invalid_password(self, service, hasher, users_repository, password):
        with pytest.raises(ValidationError):
            await service.create_one(UserCreateDto(login="bob", password=password, role_id=1))

        hasher.hash.assert_not_called()
        users_repository.create_one.assert_not_awaited()


class TestUpdateOne:
    async def test_without_password_does_not_rehash(self, service, hasher, users_repository):
        users_repository.update_one.return_value = make_user_entity(user_id=1, login="renamed")

        await service.update_one(1, UserUpdateDto(login="renamed"))

        hasher.hash.assert_not_called()
        users_repository.update_one.assert_awaited_once_with(
            entity=UserUpdateEntity(id=1, login=Login("renamed"))
        )

    async def test_with_password_rehashes(self, service, hasher, users_repository):
        users_repository.update_one.return_value = make_user_entity()

        await service.update_one(1, UserUpdateDto(password="NewPass1"))

        hasher.hash.assert_called_once_with(plain="NewPass1", salt="generated_salt")
        entity = users_repository.update_one.await_args.kwargs["entity"]
        assert entity.hashed_password == HashedPassword("generated_hash")
        assert entity.salt == Salt("generated_salt")

    async def test_invalidates_caches(self, service, cache_client, users_repository):
        users_repository.update_one.return_value = make_user_entity(user_id=1)

        await service.update_one(1, UserUpdateDto(login="renamed"))

        cache_client.delete.assert_awaited_once_with(
            patterns=["users:item:1:*:*", "users:page:*:*:*:*:*"]
        )

    async def test_raises_not_found(self, service, cache_client, users_repository):
        users_repository.update_one.return_value = None

        with pytest.raises(NotFoundError):
            await service.update_one(1, UserUpdateDto(login="renamed"))

        cache_client.delete.assert_not_awaited()

    async def test_role_change_notifies_and_reconnects_user(self, service, users_repository, connections_manager):
        new_role = make_role_entity(role_id=2, name="manager")
        users_repository.update_one.return_value = make_user_entity(user_id=1, role=new_role)
        connections_manager.get_connections.return_value = {
            # Same user, old role -> must be notified.
            100: make_connection(make_user_dto(user_id=1, role=make_role_dto(role_id=1))),
            # Other user -> ignored.
            101: make_connection(make_user_dto(user_id=2, role=make_role_dto(role_id=1)))
        }

        result = await service.update_one(1, UserUpdateDto(role_id=2))

        connections_manager.send_to_connection.assert_awaited_once_with(
            connection_id=100,
            data={
                "type": "message",
                "event": RoleEventEnum.USER_ROLE_UPDATE,
                "data": result.role.model_dump(mode="json")
            }
        )
        connections_manager.reconnect.assert_awaited_once_with(connection_id=100)

    async def test_same_role_does_not_reconnect(self, service, users_repository, connections_manager):
        users_repository.update_one.return_value = make_user_entity(user_id=1, role=make_role_entity(role_id=2))
        connections_manager.get_connections.return_value = {
            100: make_connection(make_user_dto(user_id=1, role=make_role_dto(role_id=2)))
        }

        await service.update_one(1, UserUpdateDto(role_id=2))

        connections_manager.send_to_connection.assert_not_awaited()
        connections_manager.reconnect.assert_not_awaited()

    async def test_without_role_change_skips_connections(self, service, users_repository, connections_manager):
        users_repository.update_one.return_value = make_user_entity()

        await service.update_one(1, UserUpdateDto(login="renamed"))

        connections_manager.get_connections.assert_not_awaited()


class TestDelete:
    async def test_delete_one(self, service, cache_client, users_repository):
        users_repository.delete_one.return_value = make_user_entity(user_id=4)

        await service.delete_one(4)

        users_repository.delete_one.assert_awaited_once_with(user_id=4)
        cache_client.delete.assert_awaited_once_with(
            patterns=["users:item:4:*:*", "users:page:*:*:*:*:*"]
        )

    async def test_delete_one_raises_not_found(self, service, users_repository):
        users_repository.delete_one.return_value = None

        with pytest.raises(NotFoundError):
            await service.delete_one(4)

    async def test_delete_many(self, service, cache_client, users_repository):
        users_repository.delete_many.return_value = [make_user_entity(user_id=1), make_user_entity(user_id=2)]

        await service.delete_many([1, 2])

        users_repository.delete_many.assert_awaited_once_with(user_ids=Batch([1, 2]))
        cache_client.delete.assert_awaited_once_with(
            patterns=["users:page:*:*:*:*:*", "users:item:1:*:*", "users:item:2:*:*"]
        )

    async def test_delete_many_raises_not_found(self, service, users_repository):
        users_repository.delete_many.return_value = []

        with pytest.raises(NotFoundError):
            await service.delete_many([1])
