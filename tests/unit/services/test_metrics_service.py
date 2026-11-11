#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import timedelta
from types import SimpleNamespace

import pytest

from domain.exceptions import NotFoundError
from application.mappers import MetricsServiceMapper
from application.services import MetricsService
from application.clients.metrics.shared import MetricPoint
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    MetricDiskDto,
    MetricsSubscribeServerDto,
    MetricsUnsubscribeServerDto
)

from helpers.factories import NOW


POINT = MetricPoint(value=12.5, date=NOW)


@pytest.fixture
def service(cache_client, metrics_client, connections_manager) -> MetricsService:
    return MetricsService(
        cache_client=cache_client,
        metrics_client=metrics_client,
        metrics_mapper=MetricsServiceMapper(),
        connections_manager=connections_manager
    )


@pytest.fixture
def disk_usage(monkeypatch):
    calls = []

    def fake_disk_usage(path):
        calls.append(path)
        return SimpleNamespace(free=30, total=100)

    monkeypatch.setattr("application.services.metrics.disk_usage", fake_disk_usage)
    return calls


class TestHostDisk:
    async def test_returns_cached_value(self, service, cache_client, disk_usage):
        cached = MetricDiskDto(free=1, total=2, last_check=NOW, next_check=NOW)
        cache_client.get.return_value = cached.model_dump_json()

        result = await service.host_disk()

        assert result == cached
        cache_client.get.assert_awaited_once_with(pattern=CacheConstants.METRICS_HOST_DISK_KEY)
        assert disk_usage == []

    async def test_measures_and_caches_on_miss(self, service, cache_client, disk_usage):
        result = await service.host_disk()

        assert (result.free, result.total) == (30, 100)
        assert result.next_check - result.last_check == timedelta(minutes=5)
        assert disk_usage == ["/"]
        cache_client.set.assert_awaited_once_with(
            key=CacheConstants.METRICS_HOST_DISK_KEY,
            value=result.model_dump_json(),
            expire=CacheConstants.TTL_5_MINUTES
        )

    async def test_refresh_bypasses_cache(self, service, cache_client, disk_usage):
        cache_client.get.return_value = "stale"

        result = await service.host_disk(refresh=True)

        cache_client.get.assert_not_awaited()
        assert result.free == 30


class TestHostMetrics:
    @pytest.mark.parametrize("method", ["host_last_cpu", "host_last_ram"])
    async def test_last(self, service, metrics_client, method):
        getattr(metrics_client, method).return_value = POINT

        result = await getattr(service, method)()

        assert (result.value, result.date) == (12.5, NOW)

    @pytest.mark.parametrize("method", ["host_all_cpu", "host_all_ram"])
    async def test_all(self, service, metrics_client, method):
        getattr(metrics_client, method).return_value = [POINT, MetricPoint(value=20.0, date=NOW)]

        result = await getattr(service, method)()

        assert [m.value for m in result] == [12.5, 20.0]

    @pytest.mark.parametrize(
        ("method", "empty"),
        [("host_last_cpu", None), ("host_last_ram", None), ("host_all_cpu", []), ("host_all_ram", [])]
    )
    async def test_missing_raises_not_found(self, service, metrics_client, method, empty):
        getattr(metrics_client, method).return_value = empty

        with pytest.raises(NotFoundError):
            await getattr(service, method)()


class TestServerMetrics:
    @pytest.mark.parametrize(
        ("method", "client_method", "returned"),
        [
            ("server_last_cpu", "container_last_cpu", POINT),
            ("server_last_ram", "container_last_ram", POINT),
            ("server_all_cpu", "container_all_cpu", [POINT]),
            ("server_all_ram", "container_all_ram", [POINT])
        ]
    )
    async def test_queries_runtime_container(self, service, metrics_client, method, client_method, returned):
        getattr(metrics_client, client_method).return_value = returned

        await getattr(service, method)(4)

        getattr(metrics_client, client_method).assert_awaited_once_with(container="cobalt_server_4")

    @pytest.mark.parametrize(
        ("method", "client_method", "empty"),
        [
            ("server_last_cpu", "container_last_cpu", None),
            ("server_all_ram", "container_all_ram", [])
        ]
    )
    async def test_missing_raises_with_server_id(self, service, metrics_client, method, client_method, empty):
        getattr(metrics_client, client_method).return_value = empty

        with pytest.raises(NotFoundError) as exc_info:
            await getattr(service, method)(4)

        assert exc_info.value.kwargs == {"server_id": 4}

    @pytest.mark.parametrize(("method", "client_method"), [
        ("servers_last_cpu", "containers_last_cpu"),
        ("servers_last_ram", "containers_last_ram")
    ])
    async def test_batch_keyed_by_container(self, service, metrics_client, method, client_method):
        getattr(metrics_client, client_method).return_value = {"cobalt_server_1": POINT, "cobalt_server_2": POINT}

        result = await getattr(service, method)([1, 2])

        getattr(metrics_client, client_method).assert_awaited_once_with(
            containers=["cobalt_server_1", "cobalt_server_2"]
        )
        assert set(result) == {"cobalt_server_1", "cobalt_server_2"}
        assert result["cobalt_server_1"].value == 12.5

    async def test_batch_empty_raises(self, service, metrics_client):
        metrics_client.containers_last_cpu.return_value = {}

        with pytest.raises(NotFoundError):
            await service.servers_last_cpu([1])


class TestSubscriptions:
    @pytest.mark.parametrize(("method", "room", "metric_type"), [
        ("subscribe_host_cpu", "metrics:host:cpu", "metrics_cpu"),
        ("subscribe_host_ram", "metrics:host:ram", "metrics_ram")
    ])
    async def test_host_subscribe(self, service, connections_manager, method, room, metric_type):
        await getattr(service, method)(connection_id=9)

        connections_manager.join_room.assert_awaited_once_with(
            connection_id=9, room_name=room, metadata={"type": metric_type, "target": "host"}
        )

    @pytest.mark.parametrize(("method", "room"), [
        ("unsubscribe_host_cpu", "metrics:host:cpu"),
        ("unsubscribe_host_ram", "metrics:host:ram")
    ])
    async def test_host_unsubscribe(self, service, connections_manager, method, room):
        await getattr(service, method)(connection_id=9)

        connections_manager.leave_room.assert_awaited_once_with(connection_id=9, room_name=room)

    @pytest.mark.parametrize(("method", "room", "metric_type"), [
        ("subscribe_server_cpu", "metrics:server:cpu:4", "metrics_cpu"),
        ("subscribe_server_ram", "metrics:server:ram:4", "metrics_ram")
    ])
    async def test_server_subscribe(self, service, connections_manager, method, room, metric_type):
        await getattr(service, method)(connection_id=9, dto=MetricsSubscribeServerDto(server_id=4))

        connections_manager.join_room.assert_awaited_once_with(
            connection_id=9,
            room_name=room,
            metadata={
                "type": metric_type,
                "target": "server",
                "server_id": 4,
                "container_name": "cobalt_server_4"
            }
        )

    @pytest.mark.parametrize(("method", "room"), [
        ("unsubscribe_server_cpu", "metrics:server:cpu:4"),
        ("unsubscribe_server_ram", "metrics:server:ram:4")
    ])
    async def test_server_unsubscribe(self, service, connections_manager, method, room):
        await getattr(service, method)(connection_id=9, dto=MetricsUnsubscribeServerDto(server_id=4))

        connections_manager.leave_room.assert_awaited_once_with(connection_id=9, room_name=room)
