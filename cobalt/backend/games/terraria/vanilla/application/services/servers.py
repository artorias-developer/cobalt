#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional

from application.contracts.games import AbstractServersService


class VanillaServersService(AbstractServersService):
    """
    Terraria Vanilla servers service.
    """
    _INTERNAL_PORT = 7777
    _INSTALLATION_MARKER = "TerrariaServer.bin.x86_64"

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
        - download_link: Download link for Vanilla Terraria.

        Returns:
        - None.
        """
        try:
            port = self.get_available_port()

            await self._create_installer_container(
                server_id=server_id,
                installation_marker=self._INSTALLATION_MARKER,
                image_build_args={
                    "TERRARIA_LINK": download_link
                }
            )

            await self._create_runtime_container(
                server_id=server_id,
                ports={
                    f"{self._INTERNAL_PORT}/tcp": port
                }
            )
        except Exception:
            self.logger.exception(f'Error while creating server {server_id}:')

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