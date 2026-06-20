#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Optional

from lxml import html

from application.contracts.games import (
    AbstractLoader,
    AbstractServersService
)
from application.contracts.loggers import AbstractLogger
from infrastructure.mixins import HttpClientMixin


class VanillaLoader(AbstractLoader, HttpClientMixin):
    """
    Factorio Vanilla loader.
    """
    VERSIONS_LINK: str = "https://factorio.com/download/archive/"
    DOWNLOAD_LINK: str = "https://factorio.com/get-download/{version}/headless/linux64"

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
        return [
            "1.1.69",
            "1.1.60",
            "1.1.59",
            "1.1.58",
            "1.1.57",
            "0.15.36",
            "0.11.22",
            "0.11.12",
            "0.10.12",
            "0.9.8",
            "0.8.8",
            "0.7.5",
            "0.6.4"
        ]

    def get_default_versions(self) -> List[str]:
        """
        Gets the default versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        return [
            "2.0.76",
            "2.0.73",
            "2.0.72",
            "2.0.69",
            "2.0.66",
            "2.0.60",
            "2.0.55",
            "2.0.47",
            "2.0.43",
            "2.0.42",
            "2.0.41",
            "2.0.39",
            "2.0.32",
            "2.0.30",
            "2.0.28",
            "2.0.23",
            "2.0.21",
            "2.0.20",
            "2.0.15",
            "2.0.14",
            "2.0.13",
            "2.0.12",
            "2.0.11",
            "2.0.10",
            "2.0.9",
            "2.0.8",
            "2.0.7",
            "1.1.110",
            "1.1.109",
            "1.1.107",
            "1.1.104",
            "1.1.101",
            "1.1.100",
            "1.1.94",
            "1.1.91",
            "1.1.87",
            "1.0.0",
            "0.17.79",
            "0.16.51",
            "0.15.40",
            "0.14.23",
            "0.13.20",
            "0.12.35"
        ]

    async def get_versions(self) -> List[str]:
        """
        Gets all available versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        versions = []

        response = await self.request(
            url=self.VERSIONS_LINK,
            method="GET",
        )

        if not response:
            return self.get_default_versions()

        try:
            tree = html.fromstring(response)

            elements = tree.xpath(
                "//a[contains(@class, 'version-button-stable')]/text()"
            )

            if not elements:
                return self.get_default_versions()

            unsupported_versions = self.get_unsupported_versions()

            for text in elements:
                version = text.strip()

                if version and version not in unsupported_versions:
                    versions.append(version)

        except Exception:
            self.logger.exception(f'Error while getting "{self.name}" versions:')

        if not versions:
            versions = self.get_default_versions()

        return versions

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
        return self.DOWNLOAD_LINK.format(
            version=version
        )