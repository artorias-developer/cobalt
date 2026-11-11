#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import PermissionEnum
from application.dtos import MetricDiskDto
from presentation.http.fastapi.v1.mappers import MetricsRouterMapper
from presentation.http.fastapi.v1.routers import HttpMetricsRouter

from helpers.app import build_test_client
from helpers.factories import NOW, make_metric_dto
from helpers.routes import Route, RouteContract


URL = "/api/v1/metrics"

DISK = MetricDiskDto(free=50, total=100, last_check=NOW, next_check=NOW)
METRIC = make_metric_dto()
METRICS = [make_metric_dto(10.0), make_metric_dto(20.0)]

CPU = PermissionEnum.SERVER_CPU_VIEW
RAM = PermissionEnum.SERVER_RAM_VIEW


@pytest.fixture
def service(metrics_service_mock):
    return metrics_service_mock


@pytest.fixture
def client(metrics_service_mock, auth_service_mock, i18n_manager, logger):
    with build_test_client(
        router_factories=[
            lambda api: HttpMetricsRouter(
                router=api,
                metrics_service=metrics_service_mock,
                metrics_mapper=MetricsRouterMapper(),
                auth_service=auth_service_mock
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


class TestMetricsRoutes(RouteContract):
    ROUTES = [
        Route("GET", f"{URL}/host/disk", "host_disk", [PermissionEnum.DASHBOARD_DISK_VIEW],
              call_kwargs={"refresh": False}, return_value=DISK),
        Route("GET", f"{URL}/host/cpu/last", "host_last_cpu", [PermissionEnum.DASHBOARD_CPU_VIEW],
              return_value=METRIC),
        Route("GET", f"{URL}/host/ram/last", "host_last_ram", [PermissionEnum.DASHBOARD_RAM_VIEW],
              return_value=METRIC),
        Route("GET", f"{URL}/host/cpu/all", "host_all_cpu", [PermissionEnum.DASHBOARD_CPU_VIEW],
              return_value=METRICS),
        Route("GET", f"{URL}/host/ram/all", "host_all_ram", [PermissionEnum.DASHBOARD_RAM_VIEW],
              return_value=METRICS),
        Route("GET", f"{URL}/servers/4/cpu/last", "server_last_cpu", [CPU],
              call_kwargs={"server_id": 4}, return_value=METRIC),
        Route("GET", f"{URL}/servers/4/ram/last", "server_last_ram", [RAM],
              call_kwargs={"server_id": 4}, return_value=METRIC),
        Route("GET", f"{URL}/servers/4/cpu/all", "server_all_cpu", [CPU],
              call_kwargs={"server_id": 4}, return_value=METRICS),
        Route("GET", f"{URL}/servers/4/ram/all", "server_all_ram", [RAM],
              call_kwargs={"server_id": 4}, return_value=METRICS)
    ]


class TestHostDisk:
    def test_refresh_flag_is_forwarded(self, client, login_as, metrics_service_mock):
        login_as(client)
        metrics_service_mock.host_disk.return_value = DISK

        response = client.get(f"{URL}/host/disk", params={"refresh": "true"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["free"] == 50
        assert response.json()["total"] == 100
        metrics_service_mock.host_disk.assert_awaited_once_with(refresh=True)

    def test_invalid_refresh_flag_returns_422(self, client, login_as, metrics_service_mock):
        login_as(client)

        response = client.get(f"{URL}/host/disk", params={"refresh": "maybe"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Refresh must be a valid boolean"}
        metrics_service_mock.host_disk.assert_not_awaited()


class TestSeries:
    def test_series_values_are_serialized_in_order(self, client, login_as, metrics_service_mock):
        login_as(client)
        metrics_service_mock.server_all_cpu.return_value = METRICS

        response = client.get(f"{URL}/servers/4/cpu/all")

        assert [point["value"] for point in response.json()] == [10.0, 20.0]

    def test_cpu_permission_does_not_grant_ram(self, client, login_as, metrics_service_mock):
        login_as(client, permissions=[CPU])

        response = client.get(f"{URL}/servers/4/ram/last")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        metrics_service_mock.server_last_ram.assert_not_awaited()
