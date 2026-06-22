#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import path, makedirs
from pathlib import Path

from aiofiles import os

from domain.enums import ServerStatusEnum
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.clients import AbstractContainersClient
from application.contracts.loggers import AbstractLogger
from application.contracts.services import AbstractServersService as CoreServersService
from application.contracts.games import AbstractServersService
from application.clients.containers.shared import ContainersConstants


class VanillaServersService(AbstractServersService):
    """
    7 Days to Die Vanilla servers service.
    """
    _INTERNAL_PORT = 26900

    host_containers_dir: Path

    def __init__(
        self,
        build_dir: Path,
        app_containers_dir: Path,
        host_containers_dir: Path,
        core_servers_service: CoreServersService,
        containers_client: AbstractContainersClient,
        connections_manager: AbstractConnectionsManager,
        logger: AbstractLogger
    ):
        super().__init__(
            build_dir=build_dir,
            app_containers_dir=app_containers_dir,
            core_servers_service=core_servers_service,
            containers_client=containers_client,
            connections_manager=connections_manager,
            logger=logger
        )

        self.host_containers_dir = host_containers_dir

    async def create(
        self,
        server_id: int,
        container_name: str,
        version: str,
        download_link: str
    ) -> None:
        """
        Creates a new server container.

        Parameters:
        - server_id: Server ID.
        - container_name: Container name.
        - version: Game version.
        - download_link: Download link for Vanilla 7 Days to Die.

        Returns:
        - None.
        """
        await self._update_server_status(
            server_id=server_id,
            status=ServerStatusEnum.PROCESSING
        )

        app_container_dir = path.join(self.app_containers_dir, container_name)
        host_container_dir = path.join(self.host_containers_dir, container_name)

        port_base = self.get_available_port_range(count=3)
        port_1 = port_base + 1
        port_2 = port_base + 2

        makedirs(
            name=app_container_dir,
            exist_ok=True
        )

        try:
            await self._create_installer_container(
                container_file=self._CONTAINER_INSTALLER_FILE,
                container_name=container_name,
                installation_dir=host_container_dir,
                container_kwargs={
                    "security_opt": ["seccomp=unconfined"]
                }
            )

            await self._create_runtime_container(
                container_file=self._CONTAINER_RUNTIME_FILE,
                container_name=container_name,
                ports={
                    f"{port_base}/tcp": port_base,
                    f"{port_base}/udp": port_base,
                    f"{port_1}/udp": port_1,
                    f"{port_2}/udp": port_2
                },
                volumes={
                    host_container_dir: {
                        "bind": ContainersConstants.SERVER_ROOT,
                        "mode": "rw"
                    }
                },
                container_environment={
                    "SERVER_PORT": str(port_base)
                },
                container_kwargs={
                    "security_opt": ["seccomp=unconfined"],
                    "network_mode": ContainersConstants.NETWORK_MODE
                }
            )

            if not await os.path.exists(path.join(app_container_dir, "7DaysToDieServer.x86_64")):
                raise Exception(f'Installation failed: "7DaysToDieServer.x86_64" not found in "{app_container_dir}"')

            await self._update_server_status(
                server_id=server_id,
                status=ServerStatusEnum.CREATED
            )
        except Exception:
            self.logger.exception(f'Error while creating container "{container_name}":')

            await self._remove_files(
                container_name=container_name
            )

            await self._update_server_status(
                server_id=server_id,
                status=ServerStatusEnum.FAILED
            )