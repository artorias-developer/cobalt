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
    Factorio Vanilla servers service.
    """
    _INTERNAL_PORT = 34197
    _INSTALL_MARKER = "bin/x64/factorio"

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
    ) -> tuple[int, int, int]:
        """
        Parses a version string into major, minor, and patch components.

        Parameters:
        - version: Version string (e.g. "0.12.35").

        Returns:
        - tuple[int, int, int]: Major, minor, and patch version numbers.
        """
        parts = version.split(".")
        major = int(parts[0]) if len(parts) >= 1 else 0
        minor = int(parts[1]) if len(parts) >= 2 else 0
        patch = int(parts[2]) if len(parts) >= 3 else 0

        return major, minor, patch

    def _has_admin_list_option(
        self,
        version: str
    ) -> bool:
        """
        Returns whether the given Factorio version supports the --server-adminlist flag.

        Parameters:
        - version: Factorio version.

        Returns:
        - bool: True if the version supports --server-adminlist, False otherwise.
        """
        major, minor, _ = self._parse_version(version)

        if major == 0 and minor <= 16:
            return False

        return True

    def _has_use_whitelist_option(
        self,
        version: str
    ) -> bool:
        """
        Returns whether the given Factorio version supports the --use-server-whitelist flag.

        Parameters:
        - version: Factorio version.

        Returns:
        - bool: True if the version supports --use-server-whitelist, False otherwise.
        """
        major, minor, _ = self._parse_version(version)

        if major == 0 and minor <= 16:
            return False

        return True

    def _has_whitelist_option(
        self,
        version: str
    ) -> bool:
        """
        Returns whether the given Factorio version supports the --server-whitelist flag.

        Parameters:
        - version: Factorio version.

        Returns:
        - bool: True if the version supports --server-whitelist, False otherwise.
        """
        major, minor, _ = self._parse_version(version)

        if major == 0 and minor <= 14:
            return False

        return True

    def _has_banlist_option(
        self,
        version: str
    ) -> bool:
        """
        Returns whether the given Factorio version supports the --server-banlist flag.

        Parameters:
        - version: Factorio version.

        Returns:
        - bool: True if the version supports --server-banlist, False otherwise.
        """
        major, minor, _ = self._parse_version(version)

        if major == 0 and minor <= 14:
            return False

        return True

    def _has_server_settings_option(
        self,
        version: str
    ) -> bool:
        """
        Returns whether the given Factorio version supports the --server-settings flag.

        Parameters:
        - version: Factorio version.

        Returns:
        - bool: True if the version supports --server-settings, False otherwise.
        """
        major, minor, _ = self._parse_version(version)

        if major == 0 and minor <= 12:
            return False

        return True

    def _has_relative_create_path(
        self,
        version: str
    ) -> bool:
        """
        Returns whether the given Factorio version requires a relative path for --create.

        Parameters:
        - version: Factorio version.

        Returns:
        - bool: True if the version requires a relative path, False otherwise.
        """
        major, minor, _ = self._parse_version(version)

        if major == 0 and minor <= 12:
            return True

        return False

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
        - download_link: Download link for Vanilla Factorio.

        Returns:
        - None.
        """
        await self._update_server_state(
            server_id=server_id,
            status=ServerStatusEnum.PROCESSING
        )

        host_container_dir = path.join(self.host_containers_dir, container_name)
        has_admin_list = self._has_admin_list_option(version)
        has_use_whitelist = self._has_use_whitelist_option(version)
        has_whitelist = self._has_whitelist_option(version)
        has_banlist = self._has_banlist_option(version)
        has_server_settings = self._has_server_settings_option(version)
        has_relative_create_path = self._has_relative_create_path(version)

        try:
            port = self.get_available_port()

            await self._create_container_dir(
                container_name=container_name
            )

            await self._create_installer_container(
                container_file=self._CONTAINER_INSTALLER_FILE,
                container_name=container_name,
                installation_dir=host_container_dir,
                image_build_args={
                    "FACTORIO_LINK": download_link,
                    "HAS_ADMIN_LIST_OPTION": str(has_admin_list).lower(),
                    "HAS_WHITELIST_OPTION": str(has_whitelist).lower(),
                    "HAS_BANLIST_OPTION": str(has_banlist).lower(),
                    "HAS_SERVER_SETTINGS_OPTION": str(has_server_settings).lower(),
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
                    "HAS_ADMIN_LIST_OPTION": str(has_admin_list).lower(),
                    "HAS_USE_WHITELIST_OPTION": str(has_use_whitelist).lower(),
                    "HAS_WHITELIST_OPTION": str(has_whitelist).lower(),
                    "HAS_BANLIST_OPTION": str(has_banlist).lower(),
                    "HAS_SERVER_SETTINGS_OPTION": str(has_server_settings).lower(),
                    "HAS_RELATIVE_CREATE_PATH": str(has_relative_create_path).lower()
                }
            )

            await self._update_server_state(
                server_id=server_id,
                status=ServerStatusEnum.CREATED
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
        - download_link: Download link.

        Returns:
        - None.
        """
        ...