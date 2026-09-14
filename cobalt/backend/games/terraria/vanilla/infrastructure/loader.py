#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from lxml import html

from application.contracts.games import (
    AbstractLoader,
    AbstractServersService
)
from application.contracts.clients import AbstractHttpClient
from application.contracts.loggers import AbstractLogger


class VanillaLoader(AbstractLoader):
    """
    Terraria Vanilla loader.
    """
    WIKI_LINK: str = "https://terraria.wiki.gg/wiki/Server"
    DOWNLOAD_LINK: str = "https://terraria.org/api/download/pc-dedicated-server/terraria-server-{version}.zip"

    http_client: AbstractHttpClient
    logger: AbstractLogger

    def __init__(
        self,
        game_id: int,
        name: str,
        servers_service: AbstractServersService,
        http_client: AbstractHttpClient,
        logger: AbstractLogger
    ):
        AbstractLoader.__init__(
            self,
            game_id=game_id,
            name=name,
            servers_service=servers_service
        )

        self.http_client = http_client
        self.logger = logger

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

        response = await self.http_client.request(
            url=self.WIKI_LINK,
            method="GET",
        )

        if not response:
            return self.get_default_versions()

        try:
            tree = html.fromstring(response)
            h2 = tree.xpath("//span[@id='Downloads']/ancestor::h2")[0]

            elements = []

            for sib in h2.itersiblings():
                if sib.tag == "h2":
                    break

                elements.extend(
                    sib.xpath(".//a[contains(@href, 'terraria.org') and contains(@href, 'terraria-server')]/text()")
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
            "1.4.5.8",
            "1.4.5.7",
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