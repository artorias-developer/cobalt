#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional

from application.contracts.games import AbstractServersService


class VanillaServersService(AbstractServersService):
    """
    Project Zomboid Vanilla servers service.
    """
    _INTERNAL_PORT = 16261
    _STEAM_APP_ID = 380870
    _INSTALLATION_MARKER = "start-server.sh"

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
        - download_link: Download link for Vanilla Project Zomboid.

        Returns:
        - None.
        """
        try:
            port_1 = self.get_available_port_range(count=2)
            port_2 = port_1 + 1

            await self._create_installer_container(
                server_id=server_id,
                is_steam_server=True,
                steam_app_id=self._STEAM_APP_ID,
                installation_marker=self._INSTALLATION_MARKER,
                container_environment={
                    "SERVER_DEFAULT_PORT": str(port_1),
                    "SERVER_UDP_PORT": str(port_2)

                }
            )

            await self._create_runtime_container(
                server_id=server_id,
                is_steam_server=True,
                ports={
                    f"{port_1}/udp": port_1,
                    f"{port_2}/udp": port_2
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
        - download_link: Download link for Vanilla Project Zomboid.

        Returns:
        - None.
        """
        try:
            await self._create_upgrader_container(
                server_id=server_id,
                version=version,
                is_steam_server=True,
                steam_app_id=self._STEAM_APP_ID
            )
        except Exception:
            self.logger.exception(f'Error while upgrading server {server_id}:')