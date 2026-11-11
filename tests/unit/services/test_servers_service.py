#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from shutil import which
from subprocess import run
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, sentinel

import pytest

from domain.enums import ServerStateEnum
from domain.exceptions import ConflictError, NotFoundError, ValidationError
from domain.value_objects import Batch, LoaderVersion, ServerName
from domain.entities import ServerCreateEntity, ServerUpdateEntity, ServersPageEntity
from application.mappers import (
    AttributesServiceMapper,
    GamesServiceMapper,
    LoadersServiceMapper,
    ServersServiceMapper
)
from application.services import ServersService
from application.clients.containers.shared import ContainerConstants, ContainerStatus
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    ServersGetPageDto,
    ServerCreateDto,
    ServerUpdateDto,
    ServerUpgradeDto,
    ServerExecuteDto
)

from helpers.factories import make_loader_dto, make_server_entity, make_server_dto


RUNTIME = ContainerConstants.SERVER_RUNTIME_KEY.format(server_id=1)


@pytest.fixture
def loader() -> MagicMock:
    loader = MagicMock()
    loader.get_download_link = AsyncMock(return_value="https://example.test/server.jar")
    loader.servers_service = SimpleNamespace(
        create=AsyncMock(), upgrade=AsyncMock(), delete=AsyncMock(), cancel=AsyncMock()
    )
    return loader


@pytest.fixture
def game_module(loader, containers_client) -> SimpleNamespace:
    return SimpleNamespace(
        name="minecraft",
        loaders={"vanilla": loader},
        container=SimpleNamespace(clients=SimpleNamespace(containers=containers_client))
    )


@pytest.fixture
def service(
    cache_client, connections_manager, servers_repository, loaders_service_mock,
    transactions_manager, queue, logger, game_module
) -> ServersService:
    loaders_mapper = LoadersServiceMapper()

    return ServersService(
        cache_client=cache_client,
        connections_manager=connections_manager,
        servers_repository=servers_repository,
        servers_mapper=ServersServiceMapper(
            attributes_mapper=AttributesServiceMapper(),
            games_mapper=GamesServiceMapper(loaders_mapper=loaders_mapper),
            loaders_mapper=loaders_mapper
        ),
        loaders_service=loaders_service_mock,
        transactions_manager=transactions_manager,
        queue=queue,
        logger=logger,
        game_modules={"minecraft": game_module}
    )


class TestRead:
    async def test_get_page_caches_result(self, service, cache_client, servers_repository):
        servers_repository.get_page.return_value = ServersPageEntity(
            servers=[make_server_entity()], total=1, page=1, pages=1
        )

        result = await service.get_page(ServersGetPageDto(page=1))

        assert result.servers[0].name == "survival"
        assert cache_client.set.await_args.kwargs["key"] == "servers:page:1:None:id:desc:10"

    async def test_get_page_empty_raises(self, service, servers_repository):
        servers_repository.get_page.return_value = ServersPageEntity(servers=[], total=0, page=1, pages=0)

        with pytest.raises(NotFoundError):
            await service.get_page(ServersGetPageDto(page=1))

    async def test_get_one_from_cache(self, service, cache_client, servers_repository):
        cache_client.get.return_value = make_server_dto(server_id=1).model_dump_json()

        result = await service.get_one_by_id(1)

        assert result.id == 1
        cache_client.get.assert_awaited_once_with(pattern="servers:item:1:*:*")
        servers_repository.get_one_by_id.assert_not_awaited()

    async def test_get_one_caches_with_game_and_loader(self, service, cache_client, servers_repository):
        servers_repository.get_one_by_id.return_value = make_server_entity()

        await service.get_one_by_id(1)

        assert cache_client.set.await_args.kwargs["key"] == "servers:item:1:1:1"

    async def test_get_one_missing_raises(self, service, servers_repository):
        servers_repository.get_one_by_id.return_value = None

        with pytest.raises(NotFoundError):
            await service.get_one_by_id(1)


class TestCreate:
    DTO = ServerCreateDto(name="survival", game_id=1, loader_id=1, version="1.0.0")

    async def test_creates_in_transaction_and_enqueues_install(
        self, service, loaders_service_mock, servers_repository, cache_client, queue, loader
    ):
        loaders_service_mock.get_one_by_id.return_value = make_loader_dto()
        servers_repository.create_one.return_value = make_server_entity(state=ServerStateEnum.PENDING)

        result = await service.create_one(self.DTO)

        loaders_service_mock.get_one_by_id.assert_awaited_once_with(game_id=1, loader_id=1)
        servers_repository.create_one.assert_awaited_once_with(
            entity=ServerCreateEntity(
                name=ServerName("survival"), game_id=1, loader_id=1, version=LoaderVersion("1.0.0")
            ),
            session=sentinel.session
        )
        loader.get_download_link.assert_awaited_once_with(version="1.0.0")
        cache_client.delete.assert_awaited_once_with(patterns=["servers:page:*:*:*:*:*"])
        queue.enqueue.assert_awaited_once_with(
            loader.servers_service.create,
            server_id=1,
            version="1.0.0",
            download_link="https://example.test/server.jar"
        )
        assert result.state == ServerStateEnum.PENDING

    async def test_unknown_version_is_rejected_before_db(self, service, loaders_service_mock, servers_repository):
        loaders_service_mock.get_one_by_id.return_value = make_loader_dto()

        with pytest.raises(NotFoundError):
            await service.create_one(ServerCreateDto(name="s", game_id=1, loader_id=1, version="9.9.9"))

        servers_repository.create_one.assert_not_awaited()

    async def test_loader_without_download_link(self, service, loaders_service_mock, servers_repository, queue, loader):
        loaders_service_mock.get_one_by_id.return_value = make_loader_dto()
        servers_repository.create_one.return_value = make_server_entity()
        loader.get_download_link.side_effect = NotImplementedError

        await service.create_one(self.DTO)

        assert queue.enqueue.await_args.kwargs["download_link"] is None

    async def test_download_link_failure_aborts_without_enqueue(
        self, service, loaders_service_mock, servers_repository, queue, cache_client, loader, transactions_manager
    ):
        loaders_service_mock.get_one_by_id.return_value = make_loader_dto()
        servers_repository.create_one.return_value = make_server_entity()
        loader.get_download_link.side_effect = ConnectionError("github is down")

        with pytest.raises(ConnectionError):
            await service.create_one(self.DTO)

        # The exception goes through the transaction context, so it can roll back.
        exc_type = transactions_manager.__aexit__.await_args.args[0]
        assert exc_type is ConnectionError
        queue.enqueue.assert_not_awaited()
        cache_client.delete.assert_not_awaited()

    async def test_unknown_game_module_raises(self, service, loaders_service_mock, servers_repository, queue):
        loaders_service_mock.get_one_by_id.return_value = make_loader_dto()
        servers_repository.create_one.return_value = make_server_entity(game_name="terraria")

        with pytest.raises(NotFoundError) as exc_info:
            await service.create_one(self.DTO)

        assert exc_info.value.kwargs == {"name": "terraria"}
        queue.enqueue.assert_not_awaited()


class TestUpgrade:
    @pytest.fixture
    def server_on(self, servers_repository):
        def _server_on(version="1.0.0", state=ServerStateEnum.INSTALLED, versions=None):
            entity = make_server_entity(version=version, state=state)
            if versions is not None:
                entity.loader.versions = [LoaderVersion(v) for v in versions]
            servers_repository.get_one_by_id.return_value = entity
            return entity
        return _server_on

    async def test_upgrades_to_newer_version(self, service, server_on, servers_repository, queue, loader, cache_client):
        server_on("1.0.0")
        servers_repository.update_one.return_value = make_server_entity(version="1.2.0")

        await service.upgrade_one(1, ServerUpgradeDto(version="1.2.0"))

        entity = servers_repository.update_one.await_args.kwargs["entity"]
        assert entity.version == LoaderVersion("1.2.0")
        assert entity.state == ServerStateEnum.UPGRADING
        assert servers_repository.update_one.await_args.kwargs["session"] is sentinel.session
        cache_client.delete.assert_awaited_once_with(
            patterns=["servers:item:1:*:*", "servers:page:*:*:*:*:*"]
        )
        queue.enqueue.assert_awaited_once_with(
            loader.servers_service.upgrade,
            server_id=1,
            version="1.2.0",
            download_link="https://example.test/server.jar"
        )

    @pytest.mark.parametrize(
        ("current", "target", "error"),
        [
            ("1.0.0", "1.0.0", ConflictError),  # same version
            ("1.2.0", "1.0.0", ConflictError),  # downgrade
            ("1.0.0", "2.0.0", NotFoundError)   # unknown version
        ]
    )
    async def test_rejects_invalid_target(self, service, server_on, servers_repository, current, target, error):
        server_on(current)

        with pytest.raises(error):
            await service.upgrade_one(1, ServerUpgradeDto(version=target))

        servers_repository.update_one.assert_not_awaited()

    async def test_server_on_removed_version_can_upgrade_to_any_listed(self, service, server_on, servers_repository):
        server_on("0.9.0")
        servers_repository.update_one.return_value = make_server_entity(version="1.0.0")

        await service.upgrade_one(1, ServerUpgradeDto(version="1.0.0"))

        servers_repository.update_one.assert_awaited_once()

    async def test_latest_only_loader(self, service, server_on, servers_repository):
        server_on("latest", versions=["latest"])
        servers_repository.update_one.return_value = make_server_entity(version="latest")

        await service.upgrade_one(1, ServerUpgradeDto(version="latest"))

        with pytest.raises(NotFoundError):
            await service.upgrade_one(1, ServerUpgradeDto(version="1.0.0"))

    @pytest.mark.parametrize(
        "state", [ServerStateEnum.PENDING, ServerStateEnum.INSTALLATION, ServerStateEnum.UPGRADING]
    )
    async def test_busy_server_cannot_upgrade(self, service, server_on, servers_repository, state):
        server_on("1.0.0", state=state)

        with pytest.raises(ConflictError):
            await service.upgrade_one(1, ServerUpgradeDto(version="1.2.0"))

        servers_repository.update_one.assert_not_awaited()


class TestUpdate:
    async def test_updates_name_and_invalidates_cache(self, service, servers_repository, cache_client):
        servers_repository.update_one.return_value = make_server_entity()

        await service.update_one(1, ServerUpdateDto(name="creative"))

        servers_repository.update_one.assert_awaited_once_with(
            entity=ServerUpdateEntity(id=1, name=ServerName("creative"))
        )
        cache_client.delete.assert_awaited_once_with(
            patterns=["servers:item:1:*:*", "servers:page:*:*:*:*:*"]
        )

    async def test_missing_server_raises(self, service, servers_repository, cache_client):
        servers_repository.update_one.return_value = None

        with pytest.raises(NotFoundError):
            await service.update_one(1, ServerUpdateDto(name="creative"))

        cache_client.delete.assert_not_awaited()


class TestDelete:
    async def test_delete_one_enqueues_cleanup(self, service, servers_repository, cache_client, queue, loader):
        servers_repository.get_one_by_id.return_value = make_server_entity()

        await service.delete_one(1)

        servers_repository.delete_one.assert_awaited_once_with(server_id=1)
        cache_client.delete.assert_awaited_once_with(
            patterns=["servers:item:1:*:*", "servers:page:*:*:*:*:*", "attributes:item:*:*:1"]
        )
        queue.enqueue.assert_awaited_once_with(loader.servers_service.delete, server_id=1)

    @pytest.mark.parametrize(
        "state", [ServerStateEnum.PENDING, ServerStateEnum.INSTALLATION, ServerStateEnum.UPGRADING]
    )
    async def test_busy_server_cannot_be_deleted(self, service, servers_repository, queue, state):
        servers_repository.get_one_by_id.return_value = make_server_entity(state=state)

        with pytest.raises(ConflictError):
            await service.delete_one(1)

        servers_repository.delete_one.assert_not_awaited()
        queue.enqueue.assert_not_awaited()

    async def test_delete_one_missing(self, service, servers_repository):
        servers_repository.get_one_by_id.return_value = None

        with pytest.raises(NotFoundError):
            await service.delete_one(1)

    async def test_delete_many_skips_unknown_modules_with_warning(
        self, service, servers_repository, cache_client, queue, loader, logger
    ):
        servers_repository.get_many_by_ids.return_value = [
            make_server_entity(server_id=1),
            make_server_entity(server_id=2, game_name="terraria"),
            make_server_entity(server_id=3, loader_name="paper")
        ]

        await service.delete_many([1, 2, 3])

        servers_repository.delete_many.assert_awaited_once_with(server_ids=Batch([1, 2, 3]))
        patterns = cache_client.delete.await_args.kwargs["patterns"]
        assert {"servers:item:2:*:*", "attributes:item:*:*:3"} <= set(patterns)
        queue.enqueue.assert_awaited_once_with(loader.servers_service.delete, server_id=1)
        assert logger.warning.call_count == 2

    async def test_delete_many_is_all_or_nothing_when_one_is_busy(self, service, servers_repository, queue):
        servers_repository.get_many_by_ids.return_value = [
            make_server_entity(server_id=1),
            make_server_entity(server_id=2, state=ServerStateEnum.UPGRADING)
        ]

        with pytest.raises(ConflictError):
            await service.delete_many([1, 2])

        servers_repository.delete_many.assert_not_awaited()
        queue.enqueue.assert_not_awaited()

    async def test_delete_many_none_found(self, service, servers_repository):
        servers_repository.get_many_by_ids.return_value = []

        with pytest.raises(NotFoundError):
            await service.delete_many([1])

    async def test_delete_many_rejects_empty_batch(self, service, servers_repository):
        with pytest.raises(ValidationError):
            await service.delete_many([])

        servers_repository.get_many_by_ids.assert_not_awaited()


class TestCancel:
    @pytest.mark.parametrize(
        ("state", "canceled"),
        [
            (ServerStateEnum.PENDING, ServerStateEnum.INSTALL_CANCELED),
            (ServerStateEnum.INSTALLATION, ServerStateEnum.INSTALL_CANCELED),
            (ServerStateEnum.UPGRADING, ServerStateEnum.UPGRADE_CANCELED)
        ]
    )
    async def test_cancels_running_operation(self, service, servers_repository, loader, state, canceled):
        servers_repository.get_one_by_id.return_value = make_server_entity(state=state)

        await service.cancel_one(1)

        loader.servers_service.cancel.assert_awaited_once_with(server_id=1, state=canceled)

    async def test_nothing_to_cancel(self, service, servers_repository, loader):
        servers_repository.get_one_by_id.return_value = make_server_entity(state=ServerStateEnum.INSTALLED)

        with pytest.raises(ConflictError):
            await service.cancel_one(1)

        loader.servers_service.cancel.assert_not_awaited()


class TestContainerControl:
    @pytest.fixture(autouse=True)
    def existing_server(self, servers_repository):
        servers_repository.get_one_by_id.return_value = make_server_entity()

    @pytest.mark.parametrize(
        ("method", "client_method"),
        [("start", "container_start"), ("stop", "container_stop"), ("restart", "container_restart")]
    )
    async def test_lifecycle_targets_runtime_container(self, service, containers_client, method, client_method):
        await getattr(service, method)(1)

        getattr(containers_client, client_method).assert_awaited_once_with(container_name=RUNTIME)

    async def test_unknown_game_module(self, service, servers_repository, containers_client):
        servers_repository.get_one_by_id.return_value = make_server_entity(game_name="terraria")

        with pytest.raises(NotFoundError):
            await service.start(1)

        containers_client.container_start.assert_not_awaited()

    async def test_status(self, service, containers_client):
        containers_client.container_status.return_value = ContainerStatus(running=True, port=25565)

        result = await service.status(1)

        assert (result.running, result.port) == (True, 25565)

    async def test_execute_passes_command_as_separate_argument(self, service, containers_client):
        await service.execute(1, ServerExecuteDto(command="say hello"))

        containers_client.container_execute.assert_awaited_once_with(
            container_name=RUNTIME,
            command=[
                "sh",
                "-c",
                f'printf "%s\\n" "$1" > {ContainerConstants.SERVER_FIFO}',
                "cobalt_execute",
                "say hello"
            ]
        )

    async def test_execute_script_never_contains_user_input(self, service, containers_client):
        payload = 'say "$(id)"; `id`'

        await service.execute(1, ServerExecuteDto(command=payload))

        script = containers_client.container_execute.await_args.kwargs["command"][2]
        assert payload not in script
        assert "$(" not in script and "`" not in script

    @pytest.mark.skipif(which("sh") is None, reason="requires a POSIX shell")
    @pytest.mark.parametrize(
        "payload",
        [
            'say hi"; touch {marker}; echo "',
            "say hi'; touch {marker}; echo '",
            "say $(touch {marker})",
            "say `touch {marker}`",
            "say hi && touch {marker}",
            "say hi | touch {marker}",
            'say \\"; touch {marker}; echo \\"',
            "say %s %d %n {marker}",
            "-n say hi"
        ]
    )
    async def test_execute_does_not_allow_shell_injection(
        self, service, containers_client, monkeypatch, tmp_path, payload
    ):
        # Run the exact argv the service builds through a real shell, with the FIFO
        # replaced by a regular file, and check the payload is written verbatim.
        fifo = tmp_path / "fifo"
        marker = tmp_path / "pwned"
        monkeypatch.setattr(ContainerConstants, "SERVER_FIFO", str(fifo))
        payload = payload.format(marker=marker)

        await service.execute(1, ServerExecuteDto(command=payload))
        argv = containers_client.container_execute.await_args.kwargs["command"]
        run(argv, check=True, timeout=5)

        assert not marker.exists()
        assert fifo.read_text() == payload + "\n"

    @pytest.mark.parametrize("payload", ["say hi\nop attacker", "say hi\rstop", "say\x00hi", "say\x1bhi", "say\x7f"])
    async def test_execute_rejects_control_characters(self, service, containers_client, servers_repository, payload):
        with pytest.raises(ValidationError):
            await service.execute(1, ServerExecuteDto(command=payload))

        servers_repository.get_one_by_id.assert_not_awaited()
        containers_client.container_execute.assert_not_awaited()

    async def test_execute_allows_unicode_text(self, service, containers_client):
        await service.execute(1, ServerExecuteDto(command="say Привіт, світе! ✓"))

        assert containers_client.container_execute.await_args.kwargs["command"][-1] == "say Привіт, світе! ✓"


class TestStatesSubscription:
    async def test_subscribe_and_unsubscribe(self, service, connections_manager):
        await service.subscribe_states(5)
        await service.unsubscribe_states(5)

        connections_manager.join_room.assert_awaited_once_with(connection_id=5, room_name="servers:states")
        connections_manager.leave_room.assert_awaited_once_with(connection_id=5, room_name="servers:states")
