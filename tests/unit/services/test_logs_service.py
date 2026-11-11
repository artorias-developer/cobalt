#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from asyncio import sleep as real_sleep, wait_for
from time import time_ns
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from domain.enums import EnvironmentEnum
from domain.exceptions import NotFoundError
from application.mappers import LogsServiceMapper
from application.services import LogsService
from application.clients.containers.shared import ContainerLog
from application.managers.connections.shared import Room
from application.managers.events.shared import LogEventEnum
from application.dtos import LogsSubscribeServerDto, LogsUnsubscribeServerDto

from helpers.factories import make_server_dto


HOST_CONTAINER = "dev_cobalt_backend"

# Streams start their cursor at "now", so fake Docker timestamps must be in the future.
T0 = time_ns() + 60 * 10**9


@pytest.fixture(autouse=True)
def fast_sleep(monkeypatch):
    # The streaming loop sleeps between flushes and reconnects; keep it yielding but instant.
    async def _sleep(_seconds):
        await real_sleep(0)

    monkeypatch.setattr("application.services.logs.sleep", _sleep)


@pytest.fixture
def game_module() -> SimpleNamespace:
    return SimpleNamespace(has_logs_timestamp=True)


@pytest.fixture
def service(containers_client, connections_manager, servers_service_mock, game_module) -> LogsService:
    return LogsService(
        logs_mapper=LogsServiceMapper(),
        containers_client=containers_client,
        connections_manager=connections_manager,
        servers_service=servers_service_mock,
        game_modules={"minecraft": game_module},
        app_environment=EnvironmentEnum.DEVELOPMENT
    )


class TestHistory:
    async def test_host_all_reads_backend_container(self, service, containers_client):
        containers_client.container_logs.return_value = [ContainerLog(message="a"), ContainerLog(message="b")]

        result = await service.host_all()

        containers_client.container_logs.assert_awaited_once_with(container_name=HOST_CONTAINER)
        assert [log.message for log in result] == ["a", "b"]

    async def test_host_all_empty_raises(self, service, containers_client):
        containers_client.container_logs.return_value = []

        with pytest.raises(NotFoundError):
            await service.host_all()

    @pytest.mark.parametrize(("has_timestamp", "expected_timestamps"), [(True, False), (False, True)])
    async def test_server_all_requests_docker_timestamps_only_when_game_lacks_them(
        self, service, containers_client, servers_service_mock, game_module, has_timestamp, expected_timestamps
    ):
        game_module.has_logs_timestamp = has_timestamp
        servers_service_mock.get_one_by_id.return_value = make_server_dto(server_id=3)
        containers_client.container_logs.return_value = [ContainerLog(message="x")]

        await service.server_all(3)

        containers_client.container_logs.assert_awaited_once_with(
            container_name="cobalt_server_3", timestamps=expected_timestamps
        )

    async def test_server_all_empty_raises_with_id(self, service, containers_client, servers_service_mock):
        servers_service_mock.get_one_by_id.return_value = make_server_dto(server_id=3)
        containers_client.container_logs.return_value = []

        with pytest.raises(NotFoundError) as exc_info:
            await service.server_all(3)

        assert exc_info.value.kwargs == {"server_id": 3}


class TestCursor:
    def test_first_lines_start_cursor(self, service):
        service._advance_cursor("room", [100, 200, 200])

        assert service._cursors["room"] == (200, 2)

    def test_same_timestamp_increments_count(self, service):
        service._cursors["room"] = (200, 2)

        service._advance_cursor("room", [200])

        assert service._cursors["room"] == (200, 3)

    def test_older_and_missing_timestamps_are_ignored(self, service):
        service._cursors["room"] = (200, 1)

        service._advance_cursor("room", [150, None, 300])

        assert service._cursors["room"] == (300, 1)

    def test_no_timestamps_keeps_cursor_absent(self, service):
        service._advance_cursor("room", [None])

        assert "room" not in service._cursors


async def _log_stream(logs, on_end=None):
    for log in logs:
        yield log
    if on_end:
        on_end()


class TestStreaming:
    @pytest.fixture
    def room(self, connections_manager) -> Room:
        room = Room(connections={1})
        connections_manager.get_room.return_value = room
        return room

    @pytest.fixture
    def server(self, servers_service_mock):
        servers_service_mock.get_one_by_id.return_value = make_server_dto(server_id=3)

    @staticmethod
    def _sent_messages(connections_manager):
        return [
            message
            for call in connections_manager.send_to_room.await_args_list
            for message in call.kwargs["data"]["data"]
        ]

    async def test_subscribe_server_joins_room_and_streams_logs(
        self, service, containers_client, connections_manager, room, server
    ):
        containers_client.container_stream_logs = MagicMock(side_effect=lambda **_: _log_stream(
            [ContainerLog("first", T0 + 100), ContainerLog("second", T0 + 200)],
            on_end=room.connections.clear
        ))

        await service.subscribe_server(1, LogsSubscribeServerDto(server_id=3))
        task = service._streaming_tasks["logs:server:3"]
        await wait_for(task, timeout=2)

        connections_manager.join_room.assert_awaited_once_with(
            connection_id=1,
            room_name="logs:server:3",
            metadata={
                "type": "logs", "target": "server", "server_id": 3, "container_name": "cobalt_server_3"
            }
        )
        call = connections_manager.send_to_room.await_args
        assert call.kwargs["room_name"] == "logs:server:3"
        assert call.kwargs["data"]["event"] == LogEventEnum.SERVER_LOG
        assert call.kwargs["data"]["server_id"] == 3
        assert self._sent_messages(connections_manager) == [{"message": "first"}, {"message": "second"}]
        # Finished task cleans up its registry entry and cursor.
        assert service._streaming_tasks == {}
        assert service._cursors == {}

    async def test_reconnect_resumes_from_cursor_without_duplicates(
        self, service, containers_client, connections_manager, room, server
    ):
        async def first_stream():
            yield ContainerLog("a", T0 + 100)
            yield ContainerLog("b", T0 + 200)
            yield ContainerLog("c", T0 + 200)
            raise NotFoundError("container restarted")

        streams = iter([
            first_stream(),
            # Docker's `since` is inclusive: lines at T0+200 come again and must be skipped.
            _log_stream(
                [ContainerLog("b", T0 + 200), ContainerLog("c", T0 + 200), ContainerLog("d", T0 + 300)],
                on_end=room.connections.clear
            )
        ])
        containers_client.container_stream_logs = MagicMock(side_effect=lambda **_: next(streams))

        await service.subscribe_server(1, LogsSubscribeServerDto(server_id=3))
        await wait_for(service._streaming_tasks["logs:server:3"], timeout=2)

        assert self._sent_messages(connections_manager) == [
            {"message": "a"}, {"message": "b"}, {"message": "c"}, {"message": "d"}
        ]
        second_call = containers_client.container_stream_logs.call_args_list[1]
        assert second_call.kwargs["since_nanoseconds"] == T0 + 200

    async def test_second_subscriber_reuses_running_stream(
        self, service, containers_client, connections_manager, room, server
    ):
        containers_client.container_stream_logs = MagicMock(side_effect=lambda **_: _log_stream([]))

        await service.subscribe_server(1, LogsSubscribeServerDto(server_id=3))
        first_task = service._streaming_tasks["logs:server:3"]
        await service.subscribe_server(2, LogsSubscribeServerDto(server_id=3))

        assert service._streaming_tasks["logs:server:3"] is first_task
        assert connections_manager.join_room.await_count == 2

        room.connections.clear()
        await wait_for(first_task, timeout=2)

    async def test_stream_stops_when_room_empties_mid_stream(
        self, service, containers_client, connections_manager, room
    ):
        def stream(**_):
            async def gen():
                yield ContainerLog("kept", T0 + 100)
                room.connections.clear()
                yield ContainerLog("dropped", T0 + 200)
            return gen()

        containers_client.container_stream_logs = MagicMock(side_effect=stream)

        await service.subscribe_host(1)
        await wait_for(service._streaming_tasks["logs:host"], timeout=2)

        assert {"message": "dropped"} not in self._sent_messages(connections_manager)
        assert containers_client.container_stream_logs.call_args.kwargs["container_name"] == HOST_CONTAINER

    async def test_large_batches_are_flushed_in_chunks(
        self, service, containers_client, connections_manager, room
    ):
        logs = [ContainerLog(f"line {i}", T0 + i) for i in range(250)]
        containers_client.container_stream_logs = MagicMock(
            side_effect=lambda **_: _log_stream(logs, on_end=room.connections.clear)
        )

        await service.subscribe_host(1)
        await wait_for(service._streaming_tasks["logs:host"], timeout=2)

        sizes = [len(call.kwargs["data"]["data"]) for call in connections_manager.send_to_room.await_args_list]
        assert max(sizes) <= 100
        assert sum(sizes) == 250


class TestUnsubscribe:
    async def test_unsubscribe_host(self, service, connections_manager):
        await service.unsubscribe_host(1)

        connections_manager.leave_room.assert_awaited_once_with(connection_id=1, room_name="logs:host")

    async def test_unsubscribe_server(self, service, connections_manager):
        await service.unsubscribe_server(1, LogsUnsubscribeServerDto(server_id=3))

        connections_manager.leave_room.assert_awaited_once_with(connection_id=1, room_name="logs:server:3")
