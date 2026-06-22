#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import path, makedirs
from pathlib import Path

from domain.enums import ServerStatusEnum
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.clients import AbstractContainersClient
from application.contracts.loggers import AbstractLogger
from application.contracts.services import AbstractServersService as CoreServersService
from application.contracts.games import AbstractServersService
from application.clients.containers.shared import ContainersConstants


class TModLoaderServersService(AbstractServersService):
    """
    Terraria tModLoader servers service.
    """
    _INTERNAL_PORT = 7777
    _INSTALL_MARKER = "LaunchUtils/ScriptCaller.sh"

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
        - download_link: Download link for tModLoader Terraria.

        Returns:
        - None.
        """
        await self._update_server_status(
            server_id=server_id,
            status=ServerStatusEnum.PROCESSING
        )

        app_container_dir = path.join(self.app_containers_dir, container_name)
        host_container_dir = path.join(self.host_containers_dir, container_name)

        port = self.get_available_port()

        makedirs(
            name=app_container_dir,
            exist_ok=True
        )

        try:
            await self._create_installer_container(
                container_file=self._CONTAINER_INSTALLER_FILE,
                container_name=container_name,
                installation_dir=host_container_dir,
                image_build_args={
                    "TMODLOADER_LINK": download_link
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
                    f"{self._INTERNAL_PORT}/tcp": port
                },
                volumes={
                    host_container_dir: {
                        "bind": ContainersConstants.SERVER_ROOT,
                        "mode": "rw"
                    }
                }
            )

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
