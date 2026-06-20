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
    Terraria Vanilla loader.
    """
    WIKI_LINK: str = "https://terraria.wiki.gg/wiki/Server"
    DOWNLOAD_LINK: str = "https://terraria.org/api/download/pc-dedicated-server/terraria-server-{version}.zip"

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
            "1.1.2",
            "1.0.6.1"
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
            "1.4.5.6",
            "1.4.5.5",
            "1.4.5.4",
            "1.4.5.3",
            "1.4.5.2",
            "1.4.5.1",
            "1.4.5.0",
            "1.4.4.9",
            "1.4.4.8.1",
            "1.4.4.8",
            "1.4.4.7",
            "1.4.4.6",
            "1.4.4.5",
            "1.4.4.4",
            "1.4.4.3",
            "1.4.4.2",
            "1.4.4.1",
            "1.4.4",
            "1.4.3.6",
            "1.4.3.5",
            "1.4.3.4",
            "1.4.3.3",
            "1.4.3.2",
            "1.4.3.1",
            "1.4.3",
            "1.4.2.3"
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
        unsupported_versions = self.get_unsupported_versions()

        response = await self.request(
            url=self.WIKI_LINK,
            method="GET",
        )

        if not response:
            return self.get_default_versions()

        try:
            tree = html.fromstring(response)

            elements = tree.xpath(
                "//span[@id='Downloads']/ancestor::h2/following-sibling::ul[1]//a[contains(@href, 'terraria.org') and contains(@href, 'terraria-server')]/text()"
            )

            if not elements:
                return self.get_default_versions()

            for text in elements:
                parts = text.strip().split()

                if parts:
                    version = parts[-1]

                    if version not in unsupported_versions:
                        versions.append(version)

        except Exception:
            self.logger.exception(f'Error while getting "{self.name}" versions:')

        if not versions:
            return self.get_default_versions()

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
        prepared_version = version.replace(".", "")

        return self.DOWNLOAD_LINK.format(
            version=prepared_version
        )