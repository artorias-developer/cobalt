#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import PermissionEnum
from domain.exceptions import NotFoundError
from application.dtos import LogDto
from presentation.http.fastapi.v1.mappers import LogsRouterMapper
from presentation.http.fastapi.v1.routers import HttpLogsRouter

from helpers.app import build_test_client
from helpers.routes import Route, RouteContract


URL = "/api/v1/logs"

LOGS = [LogDto(message="[INFO] Server started"), LogDto(message="[WARN] Low memory")]


@pytest.fixture
def service(logs_service_mock):
    return logs_service_mock


@pytest.fixture
def client(logs_service_mock, auth_service_mock, i18n_manager, logger):
    with build_test_client(
        router_factories=[
            lambda api: HttpLogsRouter(
                router=api,
                logs_service=logs_service_mock,
                logs_mapper=LogsRouterMapper(),
                auth_service=auth_service_mock
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


class TestLogsRoutes(RouteContract):
    ROUTES = [
        Route(
            "GET", f"{URL}/host", "host_all",
            permissions=[PermissionEnum.DASHBOARD_LOGS_VIEW],
            return_value=LOGS
        ),
        Route(
            "GET", f"{URL}/servers/5", "server_all",
            permissions=[PermissionEnum.SERVER_LOGS_VIEW],
            call_kwargs={"server_id": 5},
            return_value=LOGS
        )
    ]


class TestLogs:
    def test_host_logs_keep_order(self, client, login_as, logs_service_mock):
        login_as(client)
        logs_service_mock.host_all.return_value = LOGS

        response = client.get(f"{URL}/host")

        assert response.status_code == status.HTTP_200_OK
        assert [log["message"] for log in response.json()] == ["[INFO] Server started", "[WARN] Low memory"]

    def test_empty_server_logs(self, client, login_as, logs_service_mock):
        login_as(client)
        logs_service_mock.server_all.return_value = []

        response = client.get(f"{URL}/servers/5")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_unknown_server_returns_404(self, client, login_as, logs_service_mock):
        login_as(client)
        logs_service_mock.server_all.side_effect = NotFoundError("Server {server_id} not found", server_id=99)

        response = client.get(f"{URL}/servers/99")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "Server 99 not found"}
