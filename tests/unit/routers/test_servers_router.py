#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import (
    PermissionEnum,
    ServerSortFieldEnum,
    ServerStateEnum,
    SortDirectionEnum
)
from domain.exceptions import ConflictError, NotFoundError, ValidationError
from application.dtos import (
    ServersPageDto,
    ServersGetPageDto,
    ServerCreateDto,
    ServerUpdateDto,
    ServerUpgradeDto,
    ServerExecuteDto,
    ServerStatusDto
)
from presentation.http.fastapi.v1.mappers import (
    AttributesRouterMapper,
    GamesRouterMapper,
    LoadersRouterMapper,
    ServersRouterMapper
)
from presentation.http.fastapi.v1.routers import HttpServersRouter

from helpers.app import build_test_client
from helpers.factories import make_server_dto
from helpers.routes import Route, RouteContract


URL = "/api/v1/servers"

SERVER = make_server_dto(server_id=2)
PAGE = ServersPageDto(servers=[SERVER], total=1, page=1, pages=1)
NO_CONTENT = status.HTTP_204_NO_CONTENT


@pytest.fixture
def service(servers_service_mock):
    return servers_service_mock


@pytest.fixture
def client(servers_service_mock, auth_service_mock, i18n_manager, logger):
    loaders_mapper = LoadersRouterMapper()
    servers_mapper = ServersRouterMapper(
        attributes_mapper=AttributesRouterMapper(),
        games_mapper=GamesRouterMapper(loaders_mapper=loaders_mapper),
        loaders_mapper=loaders_mapper
    )

    with build_test_client(
        router_factories=[
            lambda api: HttpServersRouter(
                router=api,
                servers_service=servers_service_mock,
                servers_mapper=servers_mapper,
                auth_service=auth_service_mock
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


class TestServersRoutes(RouteContract):
    ROUTES = [
        Route("GET", f"{URL}/", "get_page", [PermissionEnum.SERVERS_VIEW],
              call_kwargs={"dto": ServersGetPageDto(page=1)}, return_value=PAGE),
        Route("GET", f"{URL}/2", "get_one_by_id", [PermissionEnum.SERVERS_VIEW],
              call_kwargs={"server_id": 2}, return_value=SERVER),
        Route("POST", f"{URL}/", "create_one", [PermissionEnum.SERVERS_CREATE],
              json={"name": "survival", "game_id": 1, "loader_id": 1, "version": "1.0.0"},
              call_kwargs={"dto": ServerCreateDto(name="survival", game_id=1, loader_id=1, version="1.0.0")},
              return_value=SERVER),
        Route("PATCH", f"{URL}/2", "update_one", [PermissionEnum.SERVER_UPDATE],
              json={"name": "creative"},
              call_kwargs={"server_id": 2, "dto": ServerUpdateDto(name="creative")},
              return_value=SERVER),
        Route("PATCH", f"{URL}/2/upgrade", "upgrade_one", [PermissionEnum.SERVER_SETTINGS_UPDATE],
              json={"version": "1.1.0"},
              call_kwargs={"server_id": 2, "dto": ServerUpgradeDto(version="1.1.0")},
              status=NO_CONTENT),
        Route("DELETE", f"{URL}/2", "delete_one", [PermissionEnum.SERVERS_DELETE],
              call_kwargs={"server_id": 2}, status=NO_CONTENT),
        Route("DELETE", f"{URL}/batch", "delete_many", [PermissionEnum.SERVERS_DELETE],
              json=[2, 3], call_kwargs={"server_ids": [2, 3]}, status=NO_CONTENT),
        Route("POST", f"{URL}/2/cancel", "cancel_one",
              [PermissionEnum.SERVERS_CREATE, PermissionEnum.SERVER_SETTINGS_UPDATE],
              call_kwargs={"server_id": 2}, status=NO_CONTENT),
        Route("POST", f"{URL}/2/start", "start", [PermissionEnum.SERVER_START],
              call_kwargs={"server_id": 2}, status=NO_CONTENT),
        Route("POST", f"{URL}/2/stop", "stop", [PermissionEnum.SERVER_STOP],
              call_kwargs={"server_id": 2}, status=NO_CONTENT),
        Route("POST", f"{URL}/2/restart", "restart", [PermissionEnum.SERVER_START],
              call_kwargs={"server_id": 2}, status=NO_CONTENT),
        Route("POST", f"{URL}/2/execute", "execute", [PermissionEnum.SERVER_CONSOLE_EXECUTE],
              json={"command": "say hello"},
              call_kwargs={"server_id": 2, "dto": ServerExecuteDto(command="say hello")},
              status=NO_CONTENT),
        Route("GET", f"{URL}/2/status", "status", [PermissionEnum.SERVER_VIEW],
              call_kwargs={"server_id": 2}, return_value=ServerStatusDto(running=True, port=25565))
    ]


class TestGetPage:
    def test_maps_query_and_nested_response(self, client, login_as, servers_service_mock):
        login_as(client)
        servers_service_mock.get_page.return_value = PAGE

        response = client.get(
            f"{URL}/",
            params={"page": 1, "search": "surv", "sort_field": "name", "sort_direction": "asc", "limit": 25}
        )

        assert response.status_code == status.HTTP_200_OK
        server = response.json()["servers"][0]
        assert server["name"] == "survival"
        assert server["state"] == ServerStateEnum.INSTALLED
        assert server["game"]["name"] == "minecraft"
        assert server["loader"]["name"] == "vanilla"
        assert server["attributes"][0]["key"] == "max_players"
        servers_service_mock.get_page.assert_awaited_once_with(
            dto=ServersGetPageDto(
                page=1,
                search="surv",
                sort_field=ServerSortFieldEnum.NAME,
                sort_direction=SortDirectionEnum.ASC,
                limit=25
            )
        )


class TestLifecycle:
    def test_status_of_stopped_server(self, client, login_as, servers_service_mock):
        login_as(client)
        servers_service_mock.status.return_value = ServerStatusDto(running=False)

        response = client.get(f"{URL}/2/status")

        assert response.json() == {"running": False, "port": None}

    def test_stop_permission_does_not_allow_start(self, client, login_as, servers_service_mock):
        login_as(client, permissions=[PermissionEnum.SERVER_STOP])

        assert client.post(f"{URL}/2/start").status_code == status.HTTP_403_FORBIDDEN
        assert client.post(f"{URL}/2/restart").status_code == status.HTTP_403_FORBIDDEN
        servers_service_mock.start.assert_not_awaited()
        servers_service_mock.restart.assert_not_awaited()

    def test_start_of_not_installed_server_returns_409(self, client, login_as, servers_service_mock):
        login_as(client)
        servers_service_mock.start.side_effect = ConflictError("Server is not installed")

        response = client.post(f"{URL}/2/start")

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {"message": "Server is not installed"}

    def test_unknown_server_returns_404(self, client, login_as, servers_service_mock):
        login_as(client)
        servers_service_mock.stop.side_effect = NotFoundError("Server {server_id} not found", server_id=2)

        response = client.post(f"{URL}/2/stop")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "Server 2 not found"}


class TestValidation:
    def test_create_without_version_returns_422(self, client, login_as, servers_service_mock):
        login_as(client)

        response = client.post(f"{URL}/", json={"name": "survival", "game_id": 1, "loader_id": 1})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Version is required"}
        servers_service_mock.create_one.assert_not_awaited()

    def test_create_with_non_integer_game_returns_422(self, client, login_as, servers_service_mock):
        login_as(client)

        response = client.post(
            f"{URL}/", json={"name": "survival", "game_id": "mc", "loader_id": 1, "version": "1.0.0"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Game id must be a valid integer"}

    def test_execute_without_command_returns_422(self, client, login_as, servers_service_mock):
        login_as(client)

        response = client.post(f"{URL}/2/execute", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        servers_service_mock.execute.assert_not_awaited()

    def test_unsupported_version_returns_400(self, client, login_as, servers_service_mock):
        login_as(client)
        servers_service_mock.upgrade_one.side_effect = ValidationError("Unsupported version {version}", version="9.9")

        response = client.patch(f"{URL}/2/upgrade", json={"version": "9.9"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"message": "Unsupported version 9.9"}

    def test_batch_route_is_not_shadowed_by_server_id(self, client, login_as, servers_service_mock):
        login_as(client)

        client.request("DELETE", f"{URL}/batch", json=[1])

        servers_service_mock.delete_one.assert_not_awaited()
        servers_service_mock.delete_many.assert_awaited_once_with(server_ids=[1])
