#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
Port reservation of the game servers base service.

The OS-picked candidate ports are replaced with a fixed sequence and the TCP/UDP bind check
is stubbed, so every test controls exactly which ports are tried.
"""

from asyncio import CancelledError, gather, sleep
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace
from typing import Iterable, Iterator, Set
from unittest.mock import AsyncMock, MagicMock

import pytest

import application.contracts.games.services as games_services
from domain.enums import EnvironmentEnum, ServerStateEnum
from application.contracts.games import AbstractServersService
from application.clients.containers.shared import ContainerConstants


class _ServersService(AbstractServersService):
    async def create(self, server_id, version, download_link) -> None:
        ...

    async def upgrade(self, server_id, version, download_link) -> None:
        ...


class _FakeSocket:
    """
    Stands in for socket.socket: every instance "binds" to the next candidate port.
    """
    candidates: Iterator[int] = iter(())

    def __init__(self, *args, **kwargs):
        self.port = next(self.candidates)

    def __enter__(self) -> "_FakeSocket":
        return self

    def __exit__(self, *args) -> None:
        ...

    def bind(self, address) -> None:
        ...

    def getsockname(self):
        return "0.0.0.0", self.port


@pytest.fixture(autouse=True)
def clear_reservations():
    AbstractServersService._reserved_ports.clear()
    yield
    AbstractServersService._reserved_ports.clear()


@pytest.fixture
def candidates(monkeypatch):
    """
    Sets the candidate ports the OS "hands out", in order.
    """
    def set_candidates(ports: Iterable[int]) -> None:
        monkeypatch.setattr(_FakeSocket, "candidates", iter(ports))

    monkeypatch.setattr(games_services, "socket", _FakeSocket)
    return set_candidates


@pytest.fixture
def busy_ports(monkeypatch):
    """
    Ports bound by sockets on the host machine.
    """
    ports: Set[int] = set()
    monkeypatch.setattr(
        AbstractServersService,
        "_get_host_ports",
        staticmethod(lambda: set(ports))
    )
    return ports


@pytest.fixture
def used_ports(containers_client) -> Set[int]:
    """
    Ports used by containers: published by running ones and listed in the ports label.
    """
    ports: Set[int] = set()

    async def containers_get_used_ports(ports_label: str) -> Set[int]:
        await sleep(0)
        return set(ports)

    containers_client.containers_get_used_ports.side_effect = containers_get_used_ports
    return ports


@pytest.fixture
def service(containers_client, connections_manager, logger, busy_ports, used_ports) -> _ServersService:
    core_servers_service = MagicMock()
    core_servers_service.get_one_by_id = AsyncMock(
        return_value=SimpleNamespace(state=ServerStateEnum.INSTALLATION)
    )
    core_servers_service.update_one = AsyncMock()

    return _ServersService(
        build_dir=Path("/build"),
        app_containers_dir=Path("/app/containers"),
        host_containers_dir=Path("/host/containers"),
        core_servers_service=core_servers_service,
        containers_client=containers_client,
        connections_manager=connections_manager,
        logger=logger,
        app_environment=EnvironmentEnum.DEVELOPMENT
    )


class TestReservePorts:
    async def test_single_port_is_returned_as_int(self, service, candidates):
        candidates([40000])

        port = await service.reserve_ports(server_id=1, count=1)

        assert port == 40000
        assert service._reserved_ports == {1: {40000}}

    async def test_several_ports_are_consecutive_list(self, service, candidates):
        candidates([40000])

        ports = await service.reserve_ports(server_id=1, count=3)

        assert ports == [40000, 40001, 40002]
        assert service._reserved_ports == {1: {40000, 40001, 40002}}

    @pytest.mark.parametrize("count", [0, -1])
    async def test_count_less_than_one_is_rejected(self, service, containers_client, count):
        with pytest.raises(ValueError):
            await service.reserve_ports(server_id=1, count=count)

        assert service._reserved_ports == {}
        containers_client.containers_get_used_ports.assert_not_called()

    async def test_reads_ports_label(self, service, candidates, containers_client):
        candidates([40000])

        await service.reserve_ports(server_id=1, count=1)

        containers_client.containers_get_used_ports.assert_awaited_once_with(
            ports_label=ContainerConstants.PORTS_LABEL
        )

    async def test_skips_port_used_by_container(self, service, candidates, used_ports):
        used_ports.add(40000)
        candidates([40000, 40001])

        assert await service.reserve_ports(server_id=1, count=1) == 40001

    async def test_skips_port_busy_on_machine(self, service, candidates, busy_ports):
        busy_ports.add(40000)
        candidates([40000, 40001])

        assert await service.reserve_ports(server_id=1, count=1) == 40001

    async def test_skips_port_reserved_for_another_server(self, service, candidates):
        candidates([40000, 40000, 40001])

        first = await service.reserve_ports(server_id=1, count=1)
        second = await service.reserve_ports(server_id=2, count=1)

        assert (first, second) == (40000, 40001)
        assert service._reserved_ports == {1: {40000}, 2: {40001}}

    async def test_skips_range_with_any_used_port(self, service, candidates, used_ports, busy_ports):
        used_ports.add(40002)
        busy_ports.add(40011)
        candidates([40000, 40010, 40020])

        assert await service.reserve_ports(server_id=1, count=3) == [40020, 40021, 40022]

    async def test_skips_range_past_last_port(self, service, candidates):
        candidates([65535, 40000])

        assert await service.reserve_ports(server_id=1, count=2) == [40000, 40001]

    async def test_gives_up_after_max_attempts(self, service, candidates, used_ports):
        used_ports.update({40000, 40001})
        candidates([40000, 40001, 40002])

        with pytest.raises(RuntimeError):
            await service.reserve_ports(server_id=1, count=1, max_attempts=2)

        assert service._reserved_ports == {}

    async def test_concurrent_reservations_do_not_overlap(self, service, candidates):
        candidates([40000, 40000, 40001])

        first, second = await gather(
            service.reserve_ports(server_id=1, count=1),
            service.reserve_ports(server_id=2, count=1)
        )

        assert {first, second} == {40000, 40001}

    async def test_reservation_is_shared_between_game_services(self, service, candidates, containers_client):
        other_game = _ServersService(**{
            name: getattr(service, name)
            for name in (
                "build_dir", "app_containers_dir", "host_containers_dir", "core_servers_service",
                "containers_client", "connections_manager", "logger", "app_environment"
            )
        })
        candidates([40000, 40000, 40001])

        first = await service.reserve_ports(server_id=1, count=1)
        second = await other_game.reserve_ports(server_id=2, count=1)

        assert (first, second) == (40000, 40001)


class TestReleasePorts:
    async def test_releases_only_given_server(self, service, candidates):
        candidates([40000, 40010])
        await service.reserve_ports(server_id=1, count=1)
        await service.reserve_ports(server_id=2, count=2)

        await service.release_ports(server_id=2)

        assert service._reserved_ports == {1: {40000}}

    async def test_released_port_can_be_reserved_again(self, service, candidates):
        candidates([40000, 40000])
        await service.reserve_ports(server_id=1, count=1)

        await service.release_ports(server_id=1)

        assert await service.reserve_ports(server_id=2, count=1) == 40000

    async def test_unknown_server_is_ignored(self, service):
        await service.release_ports(server_id=404)

        assert service._reserved_ports == {}


class TestRuntimeContainerPortsLabel:
    async def test_host_ports_are_written_to_label(self, service, containers_client):
        await service._create_runtime_container(
            server_id=1,
            ports={
                "7777/udp": 40001,
                "7777/tcp": "40001",
                "27015/udp": 40000
            },
            container_labels={
                "custom": "label"
            }
        )

        labels = containers_client.container_create.await_args.kwargs["labels"]

        assert labels[ContainerConstants.PORTS_LABEL] == "40000,40001"
        assert labels["custom"] == "label"


class TestGetHostPorts:
    """
    Reading ports bound on the host from the "/proc" network tables.
    """
    _HEADER = "  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n"

    def _write_tables(self, directory: Path, tables: dict) -> None:
        directory.mkdir(parents=True)

        for file_name, addresses in tables.items():
            rows = "".join(f"   0: {address} 00000000:0000 0A 0 0 0 0 0 0 1\n" for address in addresses)
            (directory / file_name).write_text(self._HEADER + rows)

    def test_ports_are_read_from_all_tables(self, tmp_path, monkeypatch):
        host_dir = tmp_path / "host"
        self._write_tables(host_dir, {
            "tcp": ["00000000:01BB", "0100007F:1F90"],
            "tcp6": ["00000000000000000000000000000000:63DD"],
            "udp": ["00000000:14E9"],
            "udp6": []
        })
        monkeypatch.setattr(ContainerConstants, "HOST_PROC_NET_DIR", str(host_dir))

        assert AbstractServersService._get_host_ports() == {443, 8080, 25565, 5353}

    def test_local_tables_are_used_without_host_mount(self, tmp_path, monkeypatch):
        local_dir = tmp_path / "local"
        self._write_tables(local_dir, {"tcp": ["00000000:1E61"]})
        monkeypatch.setattr(ContainerConstants, "HOST_PROC_NET_DIR", str(tmp_path / "missing"))
        monkeypatch.setattr(ContainerConstants, "LOCAL_PROC_NET_DIR", str(local_dir))

        assert AbstractServersService._get_host_ports() == {7777}


_GAME_SERVICES = [
    ("games.barotrauma.vanilla.application.services.servers", "1.0.0"),
    ("games.dont_starve_together.vanilla.application.services.servers", "1.0.0"),
    ("games.factorio.vanilla.application.services.servers", "1.1.110"),
    ("games.minecraft.fabric.application.services.servers", "1.20.1"),
    ("games.minecraft.forge.application.services.servers", "1.20.1"),
    ("games.minecraft.paper.application.services.servers", "1.20.1"),
    ("games.project_zomboid.vanilla.application.services.servers", "1.0.0"),
    ("games.rim_world.together.application.services.servers", "1.0.0"),
    ("games.seven_days_to_die.vanilla.application.services.servers", "1.0.0"),
    ("games.terraria.tmodloader.application.services.servers", "1.0.0"),
    ("games.terraria.vanilla.application.services.servers", "1.0.0")
]


def _game_service_class(module_name: str) -> type:
    module = import_module(module_name)

    return next(
        value for value in vars(module).values()
        if isinstance(value, type)
        and issubclass(value, AbstractServersService)
        and value is not AbstractServersService
        and value.__module__ == module_name
    )


class TestGameServicesReleasePorts:
    """
    Every game "create" must leave no reservation behind, whatever happens.
    """
    @pytest.fixture
    def game_service(self, request, service, candidates):
        module_name, version = request.param
        game_service = object.__new__(_game_service_class(module_name))
        game_service.__dict__.update(service.__dict__)
        game_service._create_installer_container = AsyncMock()
        game_service._create_runtime_container = AsyncMock()
        candidates(range(40000, 41000))

        return game_service, version

    @staticmethod
    async def _create(game_service, version: str) -> None:
        await game_service.create(server_id=1, version=version, download_link="https://example.com/server")

    @pytest.mark.parametrize("game_service", _GAME_SERVICES, indirect=True, ids=lambda param: "_".join(param[0].split(".")[1:3]))
    async def test_ports_are_held_until_runtime_is_created_and_then_released(self, game_service):
        service, version = game_service
        held = []

        async def create_runtime_container(**kwargs) -> None:
            held.append(set(AbstractServersService._reserved_ports.get(1, set())))
            assert held[0] == {int(port) for port in kwargs["ports"].values()}

        service._create_runtime_container.side_effect = create_runtime_container

        await self._create(service, version)

        assert held and held[0]
        assert AbstractServersService._reserved_ports == {}

    @pytest.mark.parametrize("game_service", _GAME_SERVICES, indirect=True, ids=lambda param: "_".join(param[0].split(".")[1:3]))
    @pytest.mark.parametrize("failing_step", ["_create_installer_container", "_create_runtime_container"])
    async def test_ports_are_released_when_a_step_fails(self, game_service, failing_step):
        service, version = game_service
        getattr(service, failing_step).side_effect = RuntimeError("boom")

        await self._create(service, version)

        assert AbstractServersService._reserved_ports == {}

    @pytest.mark.parametrize("game_service", _GAME_SERVICES, indirect=True, ids=lambda param: "_".join(param[0].split(".")[1:3]))
    async def test_ports_are_released_when_the_job_is_cancelled(self, game_service):
        service, version = game_service
        service._create_installer_container.side_effect = CancelledError()

        with pytest.raises(CancelledError):
            await self._create(service, version)

        assert AbstractServersService._reserved_ports == {}

    @pytest.mark.parametrize("game_service", _GAME_SERVICES, indirect=True, ids=lambda param: "_".join(param[0].split(".")[1:3]))
    async def test_nothing_is_left_when_reservation_fails(self, game_service, busy_ports):
        service, version = game_service
        busy_ports.update(range(1, 65536))

        await self._create(service, version)

        assert AbstractServersService._reserved_ports == {}
        service._create_runtime_container.assert_not_called()
