#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.contracts.games import (
    AbstractLoader,
    AbstractServersService
)
from application.contracts.loggers import AbstractLogger
from infrastructure.mixins import HttpClientMixin


class VanillaLoader(AbstractLoader, HttpClientMixin):
    """
    Project Zomboid Vanilla loader.
    """

    def __init__(
        self,
        game_id: int,
        name: str,
        servers_service: AbstractServersService,
        logger: AbstractLogger,
        timeout: float = 60.0
    ):
        AbstractLoader.__init__(
            self,
            game_id=game_id,
            name=name,
            servers_service=servers_service
        )

        HttpClientMixin.__init__(
            self,
            logger=logger,
            timeout=timeout
        )

    def get_unsupported_versions(self) -> List[str]:
        """
        Returns the list of unsupported versions.

        Parameters:
        - None.

        Returns:
        - List: List of unsupported versions.
        """
        return []

    def get_default_versions(self) -> List[str]:
        """
        Gets the default versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        return [
            "Latest"
        ]

    async def get_versions(self) -> List[str]:
        """
        Gets all available versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        return self.get_default_versions()

    async def get_download_link(
        self,
        version: str
    ) -> str:
        """
        Project Zomboid Dedicated Server is distributed exclusively via SteamCMD (App ID 380870). There are no
        direct download links. The installer Dockerfile handles the download using SteamCMD.

        This method exists solely to satisfy the AbstractLoader interface.
        """
        raise NotImplementedError(f"Project Zomboid does not support direct download links")