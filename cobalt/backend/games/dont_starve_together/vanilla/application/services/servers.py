#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import path
from pathlib import Path
from typing import Optional

from domain.enums import ServerStatusEnum
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.clients import AbstractContainersClient
from application.contracts.loggers import AbstractLogger
from application.contracts.services import AbstractServersService as CoreServersService
from application.contracts.games import AbstractServersService
from application.clients.containers.shared import ContainersConstants


class VanillaServersService(AbstractServersService):
    """
    Don't Starve Together Vanilla servers service.
    """
    _INTERNAL_PORT = 10999
    _STEAM_APP_ID = 343050
    _INSTALL_MARKER = "bin/dontstarve_dedicated_server_nullrenderer"

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
        download_link: Optional[str]
    ) -> None:
        """
        Creates a new server container.

        Parameters:
        - server_id: Server ID.
        - container_name: Container name.
        - version: Game version.
        - download_link: Download link for Vanilla Don't Starve Together.

        Returns:
        - None.
        """
        await self._update_server_state(
            server_id=server_id,
            status=ServerStatusEnum.PROCESSING
        )

        host_container_dir = path.join(self.host_containers_dir, container_name)

        try:
            port = self.get_available_port()

            await self._create_container_dir(
                container_name=container_name
            )

            await self._create_installer_container(
                container_file=self._CONTAINER_INSTALLER_FILE,
                container_name=container_name,
                installation_dir=host_container_dir,
                container_kwargs={
                    "security_opt": ["seccomp=unconfined"]
                },
                image_build_args={
                    "APP_ID": str(self._STEAM_APP_ID)
                }
            )

            await self._verify_installation(
                container_name=container_name,
                install_marker=self._INSTALL_MARKER
            )

            await self._create_runtime_container(
                container_file=self._CONTAINER_RUNTIME_FILE,
                container_name=container_name,
                ports={
                    f"{self._INTERNAL_PORT}/udp": port
                },
                volumes={
                    host_container_dir: {
                        "bind": ContainersConstants.SERVER_ROOT,
                        "mode": "rw"
                    }
                },
                container_environment={
                    "CONTAINER_NAME": container_name,
                    "CLUSTER_KEY": self.generate_random_key()
                },
                container_kwargs={
                    "security_opt": ["seccomp=unconfined"],
                    "network_mode": ContainersConstants.NETWORK_MODE
                }
            )

            steam_version = await self._read_steam_version(
                container_name=container_name,
                app_id=self._STEAM_APP_ID
            )

            await self._update_server_state(
                server_id=server_id,
                status=ServerStatusEnum.CREATED,
                version=steam_version
            )
        except Exception:
            self.logger.exception(f'Error while creating container "{container_name}":')

            await self._remove_container_dir(
                container_name=container_name
            )

            await self._update_server_state(
                server_id=server_id,
                status=ServerStatusEnum.FAILED
            )

    async def upgrade(
        self,
        server_id: int,
        container_name: str,
        version: str,
        download_link: Optional[str]
    ) -> None:
        """
        Upgrades an existing server container.

        Parameters:
        - server_id: Server ID.
        - container_name: Container name.
        - version: Game version.
        - download_link: Download link for Vanilla Don't Starve Together.

        Returns:
        - None.
        """
        await self._update_server_state(
            server_id=server_id,
            status=ServerStatusEnum.UPGRADING
        )

        host_container_dir = path.join(self.host_containers_dir, container_name)

        try:
            await self._create_upgrader_container(
                container_file=self._CONTAINER_UPGRADER_FILE,
                container_name=container_name,
                installation_dir=host_container_dir,
                container_kwargs={
                    "security_opt": ["seccomp=unconfined"]
                },
                image_build_args={
                    "APP_ID": str(self._STEAM_APP_ID)
                }
            )

            steam_version = await self._read_steam_version(
                container_name=container_name,
                app_id=self._STEAM_APP_ID
            )

            await self._update_server_state(
                server_id=server_id,
                status=ServerStatusEnum.CREATED,
                version=steam_version
            )
        except Exception:
            self.logger.exception(f'Error while upgrading container "{container_name}":')

            await self._update_server_state(
                server_id=server_id,
                status=ServerStatusEnum.UPGRADE_FAILED
            )

            await self.containers_client.container_start(
                container_name=container_name
            )