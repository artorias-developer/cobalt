#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, Optional, Tuple

from application.contracts.games import AbstractServersService
from games.minecraft.shared import get_java_version


class ForgeServersService(AbstractServersService):
    """
    Minecraft Forge servers service.
    """
    _INTERNAL_PORT = 25565
    _INSTALLATION_MARKER = "libraries"

    @staticmethod
    def _parse_version(
        version: str
    ) -> Tuple[int, int]:
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
        version: str,
        download_link: str
    ) -> None:
        """
        Creates a new server container.

        Parameters:
        - server_id: Server ID.
        - version: Game version.
        - download_link: Download link for Forge installer jar.

        Returns:
        - None.
        """
        java_version = get_java_version(version)
        loader_mode = self._get_loader_mode(version)
        tweak_class = self._get_tweak_class(version)

        try:
            port = await self.reserve_ports(
                server_id=server_id,
                count=1
            )

            await self._create_installer_container(
                server_id=server_id,
                installation_marker=self._INSTALLATION_MARKER,
                image_build_args={
                    "FORGE_LINK": download_link,
                    "JAVA_VERSION": java_version
                }
            )

            await self._create_runtime_container(
                server_id=server_id,
                ports={
                    f"{self._INTERNAL_PORT}/tcp": port
                },
                image_build_args={
                    "JAVA_VERSION": java_version
                },
                container_environment={
                    "LOADER_MODE": loader_mode,
                    "TWEAK_CLASS": tweak_class
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
