#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional

from application.contracts.games import AbstractServersService
from application.clients.containers.shared import ContainersConstants


class VanillaServersService(AbstractServersService):
    """
    Don't Starve Together Vanilla servers service.
    """
    _INTERNAL_PORT = 10999
    _STEAM_APP_ID = 343050
    _INSTALLATION_MARKER = "bin/dontstarve_dedicated_server_nullrenderer"

    async def create(
        self,
        server_id: int,
        version: str,
        download_link: Optional[str]
    ) -> None:
        """
        Creates a new server container.

        Parameters:
        - server_id: Server ID.
        - version: Game version.
        - download_link: Download link for Vanilla Don't Starve Together.

        Returns:
        - None.
        """
        try:
            port = self.get_available_port()

            container_name = ContainersConstants.SERVER_RUNTIME_KEY.format(
                server_id=server_id
            )

            await self._create_installer_container(
                server_id=server_id,
                is_steam_server=True,
                steam_app_id=self._STEAM_APP_ID,
                installation_marker=self._INSTALLATION_MARKER,
                container_environment={
                    "CONTAINER_NAME": container_name,
                    "CLUSTER_KEY": self.generate_random_key()
                }
            )

            await self._create_runtime_container(
                server_id=server_id,
                is_steam_server=True,
                ports={
                    f"{self._INTERNAL_PORT}/udp": port
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
        - download_link: Download link for Vanilla Don't Starve Together.

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
