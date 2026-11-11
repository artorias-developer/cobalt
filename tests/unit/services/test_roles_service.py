#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from unittest.mock import ANY

import pytest

from domain.enums import PermissionEnum
from domain.exceptions import NotFoundError, ValidationError
from domain.value_objects import Batch, RoleName
from domain.entities import (
    RoleCreateEntity,
    RoleUpdateEntity,
    RolesGetPageEntity
)
from application.mappers import RolesServiceMapper
from application.services import RolesService
from application.clients.caches.shared import CacheConstants
from application.managers.events.shared import RoleEventEnum
from application.dtos import (
    RoleDto,
    RolesPageDto,
    RolesGetPageDto,
    RoleCreateDto,
    RoleUpdateDto
)

from helpers.factories import (
    make_role_entity,
    make_roles_page_entity,
    make_role_dto,
    make_user_dto,
    make_connection
)


@pytest.fixture
def service(cache_client, roles_repository, connections_manager) -> RolesService:
    return RolesService(
        cache_client=cache_client,
        roles_repository=roles_repository,
        roles_mapper=RolesServiceMapper(),
        connections_manager=connections_manager
    )


class TestGetPage:
    async def test_returns_cached_page_without_hitting_repository(self, service, cache_client, roles_repository):
        cached = RolesPageDto(roles=[make_role_dto()], total=1, page=1, pages=1)
        cache_client.get.return_value = cached.model_dump_json()

        result = await service.get_page(RolesGetPageDto(page=1))

        assert result == cached
        cache_client.get.assert_awaited_once_with(key="roles:page:1:None:id:desc:10")
        roles_repository.get_page.assert_not_awaited()
        cache_client.set.assert_not_awaited()

    async def test_loads_from_repository_and_caches_on_miss(self, service, cache_client, roles_repository):
        roles_repository.get_page.return_value = make_roles_page_entity()

        result = await service.get_page(RolesGetPageDto(page=1, search="adm", limit=5))

        entity = roles_repository.get_page.await_args.kwargs["entity"]
        assert isinstance(entity, RolesGetPageEntity)
        assert entity.search.value == "adm"
        assert entity.limit.value == 5

        assert result.total == 1
        assert result.roles[0].name == "admin"

        cache_client.set.assert_awaited_once_with(
            key="roles:page:1:adm:id:desc:5",
            value=result.model_dump_json(),
            expire=CacheConstants.TTL_1_HOUR
        )

    async def test_raises_not_found_when_page_is_empty(self, service, roles_repository, cache_client):
        roles_repository.get_page.return_value = make_roles_page_entity(roles=[])

        with pytest.raises(NotFoundError):
            await service.get_page(RolesGetPageDto(page=1))

        cache_client.set.assert_not_awaited()

    async def test_invalid_limit_is_rejected_before_repository_call(self, service, roles_repository):
        with pytest.raises(ValidationError):
            await service.get_page(RolesGetPageDto(page=1, limit=0))

        roles_repository.get_page.assert_not_awaited()


class TestGetOneById:
    async def test_returns_cached_role(self, service, cache_client, roles_repository):
        cached = make_role_dto(role_id=7)
        cache_client.get.return_value = cached.model_dump_json()

        result = await service.get_one_by_id(7)

        assert result == cached
        cache_client.get.assert_awaited_once_with(key="roles:item:7")
        roles_repository.get_one_by_id.assert_not_awaited()

    async def test_loads_from_repository_and_caches_on_miss(self, service, cache_client, roles_repository):
        roles_repository.get_one_by_id.return_value = make_role_entity(role_id=7, name="moderator")

        result = await service.get_one_by_id(7)

        assert isinstance(result, RoleDto)
        assert (result.id, result.name) == (7, "moderator")
        roles_repository.get_one_by_id.assert_awaited_once_with(role_id=7)
        cache_client.set.assert_awaited_once_with(
            key="roles:item:7",
            value=ANY,
            expire=CacheConstants.TTL_1_HOUR
        )

    async def test_raises_not_found(self, service, roles_repository):
        roles_repository.get_one_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc_info:
            await service.get_one_by_id(42)

        assert exc_info.value.kwargs == {"role_id": 42}


class TestCreateOne:
    async def test_creates_role_and_invalidates_pages(self, service, cache_client, roles_repository):
        roles_repository.create_one.return_value = make_role_entity(role_id=3, name="manager")
        dto = RoleCreateDto(name="manager", permissions=[PermissionEnum.USERS_VIEW])

        result = await service.create_one(dto)

        roles_repository.create_one.assert_awaited_once_with(
            entity=RoleCreateEntity(
                name=RoleName("manager"),
                permissions=[PermissionEnum.USERS_VIEW]
            )
        )
        cache_client.delete.assert_awaited_once_with(patterns="roles:page:*:*:*:*:*")
        assert result.id == 3

    @pytest.mark.parametrize("name", ["", "x" * 33, "bad<name>"])
    async def test_invalid_name_is_rejected(self, service, roles_repository, name):
        with pytest.raises(ValidationError):
            await service.create_one(RoleCreateDto(name=name, permissions=[]))

        roles_repository.create_one.assert_not_awaited()


class TestUpdateOne:
    async def test_updates_role_and_invalidates_related_caches(self, service, cache_client, roles_repository):
        roles_repository.update_one.return_value = make_role_entity(role_id=5, name="renamed")

        result = await service.update_one(5, RoleUpdateDto(name="renamed"))

        roles_repository.update_one.assert_awaited_once_with(
            entity=RoleUpdateEntity(id=5, name=RoleName("renamed"), permissions=None)
        )
        cache_client.delete.assert_awaited_once_with(
            patterns=[
                "roles:item:5",
                "roles:page:*:*:*:*:*",
                "users:item:*:*:5",
                "users:page:*:*:*:*:*"
            ]
        )
        assert result.name == "renamed"

    async def test_raises_not_found_and_keeps_cache(self, service, cache_client, roles_repository):
        roles_repository.update_one.return_value = None

        with pytest.raises(NotFoundError):
            await service.update_one(5, RoleUpdateDto(name="renamed"))

        cache_client.delete.assert_not_awaited()

    async def test_notifies_and_reconnects_only_users_with_updated_role(
        self, service, roles_repository, connections_manager
    ):
        roles_repository.update_one.return_value = make_role_entity(role_id=5)
        connections_manager.get_connections.return_value = {
            10: make_connection(make_user_dto(user_id=1, role=make_role_dto(role_id=5))),
            11: make_connection(make_user_dto(user_id=2, role=make_role_dto(role_id=6)))
        }

        result = await service.update_one(5, RoleUpdateDto(permissions=[PermissionEnum.ROLES_VIEW]))

        connections_manager.send_to_connection.assert_awaited_once_with(
            connection_id=10,
            data={
                "type": "message",
                "event": RoleEventEnum.ROLE_UPDATE,
                "data": result.model_dump(mode="json")
            }
        )
        connections_manager.reconnect.assert_awaited_once_with(connection_id=10)


class TestDeleteOne:
    async def test_deletes_role_and_invalidates_caches(self, service, cache_client, roles_repository):
        roles_repository.delete_one.return_value = make_role_entity(role_id=4)

        await service.delete_one(4)

        roles_repository.delete_one.assert_awaited_once_with(role_id=4)
        patterns = cache_client.delete.await_args.kwargs["patterns"]
        assert "roles:item:4" in patterns
        assert "users:item:*:*:4" in patterns

    async def test_raises_not_found(self, service, cache_client, roles_repository):
        roles_repository.delete_one.return_value = None

        with pytest.raises(NotFoundError):
            await service.delete_one(4)

        cache_client.delete.assert_not_awaited()


class TestDeleteMany:
    async def test_deletes_roles_and_invalidates_each_item(self, service, cache_client, roles_repository):
        roles_repository.delete_many.return_value = [make_role_entity(role_id=1), make_role_entity(role_id=2)]

        await service.delete_many([1, 2])

        roles_repository.delete_many.assert_awaited_once_with(role_ids=Batch([1, 2]))
        cache_client.delete.assert_awaited_once_with(
            patterns=[
                "roles:page:*:*:*:*:*",
                "users:page:*:*:*:*:*",
                "roles:item:1",
                "users:item:*:*:1",
                "roles:item:2",
                "users:item:*:*:2"
            ]
        )

    async def test_raises_not_found_when_nothing_deleted(self, service, roles_repository):
        roles_repository.delete_many.return_value = []

        with pytest.raises(NotFoundError):
            await service.delete_many([1])

    async def test_empty_batch_is_rejected(self, service, roles_repository):
        with pytest.raises(ValidationError):
            await service.delete_many([])

        roles_repository.delete_many.assert_not_awaited()
