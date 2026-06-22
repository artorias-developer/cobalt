#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import path, makedirs
from pathlib import Path
from typing import Literal

from domain.enums import ServerStatusEnum
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.clients import AbstractContainersClient
from application.contracts.loggers import AbstractLogger
from application.contracts.services import AbstractServersService as CoreServersService
from application.contracts.games import AbstractServersService
from application.clients.containers.shared import ContainersConstants
from games.minecraft.shared import get_java_version


class ForgeServersService(AbstractServersService):
    """
    Minecraft Forge servers service.
    """
    _INTERNAL_PORT = 25565
    _INSTALL_MARKER = "libraries"

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

    @staticmethod
    def _parse_version(
        version: str
    ) -> tuple[int, int]:
        """
        Parses a version string into major and minor components.

        Parameters:
        - version: Version string (e.g. "1.12.2").

        Returns:
        - tuple[int, int]: Major and minor version numbers.
        """
        parts = version.split(".")
        major = int(parts[0]) if len(parts) >= 1 else 0
        minor = int(parts[1]) if len(parts) >= 2 else 0

        return major, minor

    def _get_loader_mode(
        self,
        version: str
    ) -> Literal["latest", "legacy", "wrapper"]:
        """
        Returns the loader mode for a given Minecraft version.

        Parameters:
        - version: Minecraft version.

        Returns:
        - Literal: Loader mode.
        """
        major, minor = self._parse_version(version)

        if major == 1 and minor <= 5:
            return "legacy"

        if major == 1 and minor <= 12:
            return "wrapper"

        if major == 1 and minor <= 16:
            return "legacy"

        return "latest"

    def _get_tweak_class(
        self,
        version: str
    ) -> Literal["cpw", "net"]:
        """
        Returns the tweak class package for a given Minecraft version.

        Parameters:
        - version: Minecraft version.

        Returns:
        - Literal: Tweak class package prefix.
        """
        major, minor = self._parse_version(version)

        if major == 1 and minor <= 7:
            return "cpw"

        return "net"

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
        - download_link: Download link for Forge installer jar.

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
        java_version = get_java_version(version)
        loader_mode = self._get_loader_mode(version)
        tweak_class = self._get_tweak_class(version)

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
                    "FORGE_LINK": download_link,
                    "JAVA_VERSION": java_version
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
                },
                image_build_args={
                    "JAVA_VERSION": java_version
                },
                container_environment={
                    "LOADER_MODE": loader_mode,
                    "TWEAK_CLASS": tweak_class
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
