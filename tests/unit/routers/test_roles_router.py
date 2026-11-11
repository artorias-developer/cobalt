#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import PermissionEnum, RoleSortFieldEnum, SortDirectionEnum
from domain.exceptions import NotFoundError, ConflictError, ValidationError
from application.dtos import (
    RolesPageDto,
    RolesGetPageDto,
    RoleCreateDto,
    RoleUpdateDto
)
from presentation.http.fastapi.v1.mappers import RolesRouterMapper
from presentation.http.fastapi.v1.routers import HttpRolesRouter

from helpers.app import build_test_client
from helpers.factories import make_role_dto


URL = "/api/v1/roles"


@pytest.fixture
def client(roles_service_mock, auth_service_mock, i18n_manager, logger):
    with build_test_client(
        router_factories=[
            lambda api: HttpRolesRouter(
                router=api,
                roles_service=roles_service_mock,
                roles_mapper=RolesRouterMapper(),
                auth_service=auth_service_mock
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


class TestAccess:
    def test_without_session_returns_401(self, client, roles_service_mock):
        response = client.get(f"{URL}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"message": "Invalid session"}
        roles_service_mock.get_page.assert_not_awaited()

    def test_invalid_session_returns_401(self, client, auth_service_mock):
        client.cookies.set("session_id", "expired")
        auth_service_mock.get_session_user.return_value = None

        response = client.get(f"{URL}/1")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        auth_service_mock.get_session_user.assert_awaited_once_with(session_id="expired")

    @pytest.mark.parametrize(
        ("method", "path", "body"),
        [
            ("GET", "/1", None),
            ("POST", "/", {"name": "x", "permissions": []}),
            ("PATCH", "/1", {"name": "x"}),
            ("DELETE", "/1", None),
            ("DELETE", "/batch", [1])
        ]
    )
    def test_missing_permission_returns_403(self, client, login_as, roles_service_mock, method, path, body):
        login_as(client, permissions=[PermissionEnum.DASHBOARD_VIEW])

        response = client.request(method, f"{URL}{path}", json=body)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"message": "Not enough permissions"}
        assert not any(m.await_count for m in (
            roles_service_mock.get_one_by_id,
            roles_service_mock.create_one,
            roles_service_mock.update_one,
            roles_service_mock.delete_one,
            roles_service_mock.delete_many
        ))

    @pytest.mark.parametrize(
        "permission",
        [PermissionEnum.ROLES_VIEW, PermissionEnum.USERS_CREATE, PermissionEnum.USERS_UPDATE]
    )
    def test_get_page_allows_any_of_permissions(self, client, login_as, roles_service_mock, permission):
        login_as(client, permissions=[permission])
        roles_service_mock.get_page.return_value = RolesPageDto(roles=[], total=0, page=1, pages=0)

        response = client.get(f"{URL}/")

        assert response.status_code == status.HTTP_200_OK


class TestGetPage:
    def test_passes_query_to_service(self, client, login_as, roles_service_mock):
        login_as(client)
        roles_service_mock.get_page.return_value = RolesPageDto(
            roles=[make_role_dto(role_id=2, name="manager")], total=1, page=2, pages=2
        )

        response = client.get(
            f"{URL}/",
            params={"page": 2, "search": "man", "sort_field": "name", "sort_direction": "asc", "limit": 5}
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["total"] == 1
        assert body["roles"][0]["name"] == "manager"
        roles_service_mock.get_page.assert_awaited_once_with(
            dto=RolesGetPageDto(
                page=2,
                search="man",
                sort_field=RoleSortFieldEnum.NAME,
                sort_direction=SortDirectionEnum.ASC,
                limit=5
            )
        )

    def test_invalid_sort_field_returns_422(self, client, login_as, roles_service_mock):
        login_as(client)

        response = client.get(f"{URL}/", params={"sort_field": "password"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert "message" in response.json()
        roles_service_mock.get_page.assert_not_awaited()

    def test_not_found_maps_to_404(self, client, login_as, roles_service_mock):
        login_as(client)
        roles_service_mock.get_page.side_effect = NotFoundError("Roles not found")

        response = client.get(f"{URL}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "Roles not found"}


class TestGetOne:
    def test_returns_role(self, client, login_as, roles_service_mock):
        login_as(client)
        roles_service_mock.get_one_by_id.return_value = make_role_dto(role_id=3, name="mod")

        response = client.get(f"{URL}/3")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 3
        assert response.json()["name"] == "mod"
        roles_service_mock.get_one_by_id.assert_awaited_once_with(role_id=3)

    def test_not_found_message_is_formatted(self, client, login_as, roles_service_mock):
        login_as(client)
        roles_service_mock.get_one_by_id.side_effect = NotFoundError("Role {role_id} not found", role_id=3)

        response = client.get(f"{URL}/3")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "Role 3 not found"}

    def test_non_integer_id_returns_422(self, client, login_as, roles_service_mock):
        login_as(client)

        response = client.get(f"{URL}/abc")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Role id must be a valid integer"}
        roles_service_mock.get_one_by_id.assert_not_awaited()


class TestCreateOne:
    def test_creates_role(self, client, login_as, roles_service_mock):
        login_as(client)
        roles_service_mock.create_one.return_value = make_role_dto(
            role_id=10, name="manager", permissions=[PermissionEnum.USERS_VIEW]
        )

        response = client.post(f"{URL}/", json={"name": "manager", "permissions": ["users_view"]})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["permissions"] == ["users_view"]
        roles_service_mock.create_one.assert_awaited_once_with(
            dto=RoleCreateDto(name="manager", permissions=[PermissionEnum.USERS_VIEW])
        )

    def test_missing_name_returns_422(self, client, login_as, roles_service_mock):
        login_as(client)

        response = client.post(f"{URL}/", json={"permissions": []})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Name is required"}
        roles_service_mock.create_one.assert_not_awaited()

    def test_unknown_permission_returns_422(self, client, login_as, roles_service_mock):
        login_as(client)

        response = client.post(f"{URL}/", json={"name": "x", "permissions": ["god_mode"]})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        roles_service_mock.create_one.assert_not_awaited()

    def test_domain_validation_error_maps_to_400(self, client, login_as, roles_service_mock):
        login_as(client)
        roles_service_mock.create_one.side_effect = ValidationError("Invalid name")

        response = client.post(f"{URL}/", json={"name": "<bad>", "permissions": []})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"message": "Invalid name"}

    def test_conflict_maps_to_409(self, client, login_as, roles_service_mock):
        login_as(client)
        roles_service_mock.create_one.side_effect = ConflictError("Role already exists")

        response = client.post(f"{URL}/", json={"name": "admin", "permissions": []})

        assert response.status_code == status.HTTP_409_CONFLICT


class TestUpdateOne:
    def test_partial_update(self, client, login_as, roles_service_mock):
        login_as(client)
        roles_service_mock.update_one.return_value = make_role_dto(role_id=4, name="renamed")

        response = client.patch(f"{URL}/4", json={"name": "renamed"})

        assert response.status_code == status.HTTP_200_OK
        roles_service_mock.update_one.assert_awaited_once_with(
            role_id=4,
            dto=RoleUpdateDto(name="renamed", permissions=None)
        )


class TestDelete:
    def test_delete_one_returns_204(self, client, login_as, roles_service_mock):
        login_as(client)

        response = client.delete(f"{URL}/4")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b""
        roles_service_mock.delete_one.assert_awaited_once_with(role_id=4)

    def test_delete_many_returns_204(self, client, login_as, roles_service_mock):
        login_as(client)

        response = client.request("DELETE", f"{URL}/batch", json=[1, 2, 3])

        assert response.status_code == status.HTTP_204_NO_CONTENT
        roles_service_mock.delete_many.assert_awaited_once_with(role_ids=[1, 2, 3])

    def test_delete_many_with_invalid_body_returns_422(self, client, login_as, roles_service_mock):
        login_as(client)

        response = client.request("DELETE", f"{URL}/batch", json={"ids": [1]})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        roles_service_mock.delete_many.assert_not_awaited()

    def test_unexpected_error_returns_500_and_is_logged(self, client, login_as, roles_service_mock, logger):
        login_as(client)
        roles_service_mock.delete_one.side_effect = RuntimeError("db is down")

        response = client.delete(f"{URL}/4")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"message": "Internal server error"}
        logger.exception.assert_called_once()
