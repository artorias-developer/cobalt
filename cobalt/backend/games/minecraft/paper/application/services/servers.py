#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional

from application.contracts.games import AbstractServersService
from games.minecraft.shared import get_java_version


class PaperServersService(AbstractServersService):
    """
    Minecraft Paper servers service.
    """
    _INTERNAL_PORT = 25565
    _INSTALLATION_MARKER = "paper-server.jar"

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
        - download_link: Download link for Paper server jar.

        Returns:
        - None.
        """
        java_version = get_java_version(version)

        try:
            port = await self.reserve_ports(
                server_id=server_id,
                count=1
            )

            await self._create_installer_container(
                server_id=server_id,
                installation_marker=self._INSTALLATION_MARKER,
                image_build_args={
                    "PAPER_LINK": download_link
                }
            )

            await self._create_runtime_container(
                server_id=server_id,
                ports={
                    f"{self._INTERNAL_PORT}/tcp": port
                },
                image_build_args={
                    "JAVA_VERSION": java_version
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