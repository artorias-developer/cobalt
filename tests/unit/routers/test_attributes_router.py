#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import PermissionEnum
from domain.exceptions import ConflictError, NotFoundError
from application.dtos import (
    AttributesPageDto,
    AttributesGetPageDto,
    AttributeCreateDto,
    AttributeUpdateDto
)
from presentation.http.fastapi.v1.mappers import AttributesRouterMapper
from presentation.http.fastapi.v1.routers import HttpAttributesRouter

from helpers.app import build_test_client
from helpers.factories import make_attribute_dto
from helpers.routes import Route, RouteContract


SERVER_ID = 3
URL = f"/api/v1/servers/{SERVER_ID}/attributes"

VIEW = PermissionEnum.SERVER_SETTINGS_VIEW
UPDATE = PermissionEnum.SERVER_SETTINGS_UPDATE

ATTRIBUTE = make_attribute_dto(server_id=SERVER_ID)
PAGE = AttributesPageDto(attributes=[ATTRIBUTE], total=1, page=1, pages=1)


@pytest.fixture
def service(attributes_service_mock):
    return attributes_service_mock


@pytest.fixture
def client(attributes_service_mock, auth_service_mock, i18n_manager, logger):
    with build_test_client(
        router_factories=[
            lambda api: HttpAttributesRouter(
                router=api,
                attributes_service=attributes_service_mock,
                attributes_mapper=AttributesRouterMapper(),
                auth_service=auth_service_mock
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


class TestAttributesRoutes(RouteContract):
    ROUTES = [
        Route(
            "GET", f"{URL}/", "get_page", [VIEW],
            call_kwargs={"server_id": SERVER_ID, "dto": AttributesGetPageDto(page=1)},
            return_value=PAGE
        ),
        Route(
            "GET", f"{URL}/1", "get_one_by_id", [VIEW],
            call_kwargs={"server_id": SERVER_ID, "attribute_id": 1},
            return_value=ATTRIBUTE
        ),
        Route(
            "POST", f"{URL}/", "create_one", [UPDATE],
            json={"key": "max_players", "value": "10"},
            call_kwargs={"server_id": SERVER_ID, "dto": AttributeCreateDto(key="max_players", value="10")},
            return_value=ATTRIBUTE
        ),
        Route(
            "POST", f"{URL}/batch", "create_many", [UPDATE],
            json=[{"key": "a", "value": "1"}, {"key": "b", "value": "2"}],
            call_kwargs={
                "server_id": SERVER_ID,
                "dtos": [AttributeCreateDto(key="a", value="1"), AttributeCreateDto(key="b", value="2")]
            },
            return_value=[ATTRIBUTE]
        ),
        Route(
            "PATCH", f"{URL}/1", "update_one", [UPDATE],
            json={"value": "20"},
            call_kwargs={"server_id": SERVER_ID, "dto": AttributeUpdateDto(id=1, key=None, value="20")},
            return_value=ATTRIBUTE
        ),
        Route(
            "PATCH", f"{URL}/batch", "update_many", [UPDATE],
            json=[{"id": 1, "value": "20"}, {"id": 2, "key": "renamed"}],
            call_kwargs={
                "server_id": SERVER_ID,
                "dtos": [AttributeUpdateDto(id=1, value="20"), AttributeUpdateDto(id=2, key="renamed")]
            },
            return_value=[ATTRIBUTE]
        ),
        Route(
            "DELETE", f"{URL}/1", "delete_one", [UPDATE],
            call_kwargs={"server_id": SERVER_ID, "attribute_id": 1},
            status=status.HTTP_204_NO_CONTENT
        ),
        Route(
            "DELETE", f"{URL}/batch", "delete_many", [UPDATE],
            json=[1, 2],
            call_kwargs={"server_id": SERVER_ID, "attribute_ids": [1, 2]},
            status=status.HTTP_204_NO_CONTENT
        )
    ]


class TestAttributes:
    def test_view_permission_does_not_allow_changes(self, client, login_as, attributes_service_mock):
        login_as(client, permissions=[VIEW])

        response = client.post(f"{URL}/", json={"key": "a", "value": "1"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        attributes_service_mock.create_one.assert_not_awaited()

    def test_get_one_returns_attribute(self, client, login_as, attributes_service_mock):
        login_as(client)
        attributes_service_mock.get_one_by_id.return_value = ATTRIBUTE

        body = client.get(f"{URL}/1").json()

        assert (body["server_id"], body["key"], body["value"]) == (SERVER_ID, "max_players", "10")

    def test_create_without_value_returns_422(self, client, login_as, attributes_service_mock):
        login_as(client)

        response = client.post(f"{URL}/", json={"key": "a"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Value is required"}
        attributes_service_mock.create_one.assert_not_awaited()

    def test_update_many_requires_ids(self, client, login_as, attributes_service_mock):
        login_as(client)

        response = client.patch(f"{URL}/batch", json=[{"value": "1"}])

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Id is required"}
        attributes_service_mock.update_many.assert_not_awaited()

    def test_create_many_requires_list(self, client, login_as, attributes_service_mock):
        login_as(client)

        response = client.post(f"{URL}/batch", json={"key": "a", "value": "1"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        attributes_service_mock.create_many.assert_not_awaited()

    def test_duplicate_key_returns_409(self, client, login_as, attributes_service_mock):
        login_as(client)
        attributes_service_mock.create_one.side_effect = ConflictError("Attribute already exists")

        response = client.post(f"{URL}/", json={"key": "a", "value": "1"})

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_unknown_server_returns_404(self, client, login_as, attributes_service_mock):
        login_as(client)
        attributes_service_mock.get_page.side_effect = NotFoundError("Server {server_id} not found", server_id=3)

        response = client.get(f"{URL}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "Server 3 not found"}
