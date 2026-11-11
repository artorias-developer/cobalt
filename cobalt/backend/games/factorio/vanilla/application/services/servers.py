#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, Tuple

from application.contracts.games import AbstractServersService


class VanillaServersService(AbstractServersService):
    """
    Factorio Vanilla servers service.
    """
    _INTERNAL_PORT = 34197
    _INSTALLATION_MARKER = "bin/x64/factorio"

    @staticmethod
    def _parse_version(
        version: str
    ) -> Tuple[int, int, int]:
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
        version: str,
        download_link: str
    ) -> None:
        """
        Creates a new server container.

        Parameters:
        - server_id: Server ID.
        - version: Game version.
        - download_link: Download link for Vanilla Factorio.

        Returns:
        - None.
        """
        has_admin_list = self._has_admin_list_option(version)
        has_use_whitelist = self._has_use_whitelist_option(version)
        has_whitelist = self._has_whitelist_option(version)
        has_banlist = self._has_banlist_option(version)
        has_server_settings = self._has_server_settings_option(version)
        has_relative_create_path = self._has_relative_create_path(version)

        try:
            port = await self.reserve_ports(
                server_id=server_id,
                count=1
            )

            await self._create_installer_container(
                server_id=server_id,
                installation_marker=self._INSTALLATION_MARKER,
                image_build_args={
                    "FACTORIO_LINK": download_link,
                },
                container_environment={
                    "HAS_ADMIN_LIST_OPTION": str(has_admin_list).lower(),
                    "HAS_WHITELIST_OPTION": str(has_whitelist).lower(),
                    "HAS_BANLIST_OPTION": str(has_banlist).lower(),
                    "HAS_SERVER_SETTINGS_OPTION": str(has_server_settings).lower(),
                }
            )

            await self._create_runtime_container(
                server_id=server_id,
                ports={
                    f"{self._INTERNAL_PORT}/udp": port
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
        except Exception:
            self.logger.exception(f'Error while creating server {server_id}:')
        finally:
            await self.release_ports(
                server_id=server_id
            )

    async def upgrade(
        self,
        server_id: int,
        version: str,
        download_link: Optional[str]
    ) -> None:
        """
        Upgrades an existing server container.

        Parameters:
        - server_id: Server ID.
        - version: Game version.
        - download_link: Download link.

        Returns:
        - None.
        """
        ...