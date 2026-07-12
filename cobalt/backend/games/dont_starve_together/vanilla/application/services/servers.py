#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import path
from pathlib import Path
from typing import Optional

from application.contracts.managers import AbstractConnectionsManager
from application.contracts.clients import AbstractContainersClient
from application.contracts.loggers import AbstractLogger
from application.contracts.services import AbstractServersService as CoreServersService
from application.contracts.games import AbstractServersService


class VanillaServersService(AbstractServersService):
    """
    Don't Starve Together Vanilla servers service.
    """
    _INTERNAL_PORT = 10999
    _STEAM_APP_ID = 343050
    _INSTALLATION_MARKER = "bin/dontstarve_dedicated_server_nullrenderer"

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
        host_container_dir = path.join(self.host_containers_dir, container_name)

        try:
            port = self.get_available_port()

            await self._create_installer_container(
                server_id=server_id,
                is_steam_server=True,
                steam_app_id=self._STEAM_APP_ID,
                container_name=container_name,
                installation_dir=host_container_dir,
                installation_marker=self._INSTALLATION_MARKER
            )

            await self._create_runtime_container(
                server_id=server_id,
                is_steam_server=True,
                container_name=container_name,
                installation_dir=host_container_dir,
                ports={
                    f"{self._INTERNAL_PORT}/udp": port
                },
                container_environment={
                    "CONTAINER_NAME": container_name,
                    "CLUSTER_KEY": self.generate_random_key()
                }
            )
        except Exception:
            self.logger.exception(f'Error while creating container "{container_name}":')

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
        host_container_dir = path.join(self.host_containers_dir, container_name)

        try:
            await self._create_upgrader_container(
                server_id=server_id,
                version=version,
                is_steam_server=True,
                steam_app_id=self._STEAM_APP_ID,
                container_name=container_name,
                installation_dir=host_container_dir
            )
        except Exception:
            self.logger.exception(f'Error while upgrading container "{container_name}":')
