#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import PermissionEnum
from domain.exceptions import NotFoundError, ConflictError
from application.dtos import (
    UsersPageDto,
    UserCreateDto,
    UserUpdateDto
)
from presentation.http.fastapi.v1.mappers import (
    RolesRouterMapper,
    SettingsRouterMapper,
    UsersRouterMapper
)
from presentation.http.fastapi.v1.routers import HttpUsersRouter

from helpers.app import build_test_client
from helpers.factories import make_user_dto


URL = "/api/v1/users"


@pytest.fixture
def client(users_service_mock, auth_service_mock, i18n_manager, logger):
    users_mapper = UsersRouterMapper(
        roles_mapper=RolesRouterMapper(),
        settings_mapper=SettingsRouterMapper()
    )

    with build_test_client(
        router_factories=[
            lambda api: HttpUsersRouter(
                router=api,
                users_service=users_service_mock,
                users_mapper=users_mapper,
                auth_service=auth_service_mock
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


class TestGetMe:
    def test_requires_session(self, client):
        response = client.get(f"{URL}/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_works_without_any_permissions(self, client, login_as, users_service_mock):
        user = login_as(client, permissions=[], user_id=7)

        response = client.get(f"{URL}/me")

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["id"] == 7
        assert body["login"] == user.login
        assert body["settings"]["language"] == "en"
        users_service_mock.get_one_by_id.assert_not_awaited()

    def test_never_exposes_password_hash_or_salt(self, client, login_as):
        login_as(client)

        body = client.get(f"{URL}/me").json()

        assert "hashed_password" not in body
        assert "salt" not in body


class TestGetPage:
    def test_requires_users_view(self, client, login_as, users_service_mock):
        login_as(client, permissions=[PermissionEnum.ROLES_VIEW])

        response = client.get(f"{URL}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        users_service_mock.get_page.assert_not_awaited()

    def test_returns_page_without_secrets(self, client, login_as, users_service_mock):
        login_as(client)
        users_service_mock.get_page.return_value = UsersPageDto(
            users=[make_user_dto(user_id=1), make_user_dto(user_id=2, login="alice")],
            total=2, page=1, pages=1
        )

        response = client.get(f"{URL}/")

        assert response.status_code == status.HTTP_200_OK
        users = response.json()["users"]
        assert [u["login"] for u in users] == ["john_doe", "alice"]
        assert all("hashed_password" not in u and "salt" not in u for u in users)


class TestGetOne:
    def test_returns_user(self, client, login_as, users_service_mock):
        login_as(client)
        users_service_mock.get_one_by_id.return_value = make_user_dto(user_id=5, login="bob")

        response = client.get(f"{URL}/5")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["login"] == "bob"
        users_service_mock.get_one_by_id.assert_awaited_once_with(user_id=5)

    def test_not_found(self, client, login_as, users_service_mock):
        login_as(client)
        users_service_mock.get_one_by_id.side_effect = NotFoundError("User {user_id} not found", user_id=5)

        response = client.get(f"{URL}/5")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "User 5 not found"}


class TestCreateOne:
    def test_creates_user(self, client, login_as, users_service_mock):
        login_as(client)
        users_service_mock.create_one.return_value = make_user_dto(user_id=9, login="bob")

        response = client.post(f"{URL}/", json={"login": "bob", "password": "Secret123", "role_id": 2})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 9
        users_service_mock.create_one.assert_awaited_once_with(
            dto=UserCreateDto(login="bob", password="Secret123", role_id=2)
        )

    def test_missing_role_returns_422(self, client, login_as, users_service_mock):
        login_as(client)

        response = client.post(f"{URL}/", json={"login": "bob", "password": "Secret123"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Role id is required"}
        users_service_mock.create_one.assert_not_awaited()

    def test_duplicate_login_returns_409(self, client, login_as, users_service_mock):
        login_as(client)
        users_service_mock.create_one.side_effect = ConflictError("User already exists")

        response = client.post(f"{URL}/", json={"login": "bob", "password": "Secret123", "role_id": 2})

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_requires_users_create(self, client, login_as, users_service_mock):
        login_as(client, permissions=[PermissionEnum.USERS_VIEW])

        response = client.post(f"{URL}/", json={"login": "bob", "password": "Secret123", "role_id": 2})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        users_service_mock.create_one.assert_not_awaited()


class TestUpdateAndDelete:
    def test_update_one(self, client, login_as, users_service_mock):
        login_as(client)
        users_service_mock.update_one.return_value = make_user_dto(user_id=3)

        response = client.patch(f"{URL}/3", json={"role_id": 2})

        assert response.status_code == status.HTTP_200_OK
        users_service_mock.update_one.assert_awaited_once_with(
            user_id=3,
            dto=UserUpdateDto(login=None, password=None, role_id=2)
        )

    def test_delete_one(self, client, login_as, users_service_mock):
        login_as(client)

        response = client.delete(f"{URL}/3")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        users_service_mock.delete_one.assert_awaited_once_with(user_id=3)

    def test_delete_many(self, client, login_as, users_service_mock):
        login_as(client)

        response = client.request("DELETE", f"{URL}/batch", json=[3, 4])

        assert response.status_code == status.HTTP_204_NO_CONTENT
        users_service_mock.delete_many.assert_awaited_once_with(user_ids=[3, 4])

    def test_batch_route_is_not_shadowed_by_user_id(self, client, login_as, users_service_mock):
        login_as(client)

        client.request("DELETE", f"{URL}/batch", json=[1])

        users_service_mock.delete_one.assert_not_awaited()
