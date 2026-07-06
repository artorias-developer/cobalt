#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List

from .services import AbstractServersService


class AbstractLoader(ABC):
    """
    Abstract loader.
    """
    game_id: int
    name: str
    servers_service: AbstractServersService

    def __init__(
        self,
        game_id: int,
        name: str,
        servers_service: AbstractServersService
    ):
        self.game_id = game_id
        self.name = name
        self.servers_service = servers_service

    @staticmethod
    def get_unsupported_versions() -> List[str]:
        """
        Returns the list of unsupported versions.

        Parameters:
        - None.

        Returns:
        - List: List of unsupported versions.
        """
        ...

    @abstractmethod
    def get_default_versions(self) -> List[str]:
        """
        Gets the default versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        ...

    @abstractmethod
    async def get_versions(self) -> List[str]:
        """
        Gets all available versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        ...

    @abstractmethod
    async def get_download_link(
        self,
        version: str
    ) -> str:
        """
        Gets a link for download.

        Parameters:
        - version: Game version.

        Returns:
        - str: Download URL.
        """
        ...
