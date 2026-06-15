#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Optional

from application.contracts.games import (
    AbstractLoader,
    AbstractServersService
)
from application.contracts.loggers import AbstractLogger
from infrastructure.mixins import HttpClientMixin


class TogetherLoader(AbstractLoader, HttpClientMixin):
    """
    RimWorld Together loader.
    """
    GITHUB_API = "https://api.github.com/repos/RimWorld-Together/Rimworld-Together/releases"
    DOWNLOAD_LINK = "https://github.com/RimWorld-Together/Rimworld-Together/releases/download/{version}/linux-x64.zip"

    def __init__(
        self,
        game_id: int,
        name: str,
        logger: AbstractLogger,
        servers_service: AbstractServersService,
        timeout: Optional[float] = 60.0
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
            "24.9.1.1.Patcher.Fix",
            "1.5.0",
            "1.4.0",
            "1.3.2",
            "1.3.1",
            "1.3.0",
            "1.2.0"
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
           "26.6.9.1",
           "26.6.8.1",
           "26.5.24.1",
           "26.4.18.1",
           "26.4.1.1",
           "26.3.30.1",
           "26.3.28.1",
           "26.3.27.1",
           "26.3.23.1",
           "26.3.6.1",
           "26.2.13.1",
           "26.1.18.1",
           "26.1.3.1",
           "25.12.19.1",
           "25.12.16.1",
           "25.12.14.1",
           "25.12.13.1",
           "25.7.11.1",
           "25.6.28.1",
           "25.5.9.1",
           "25.3.9.1",
           "25.1.31.1",
           "25.1.2.1",
           "24.11.5.1",
           "24.11.2.1",
           "24.10.6.1",
           "24.9.1.1",
           "24.8.31.1",
           "24.7.19.1",
           "24.6.28.1",
           "24.6.23.1",
           "24.6.8.1",
           "24.6.7.1"
        ]

    async def get_versions(self) -> List[str]:
        """
        Gets all available versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        default_versions = self.get_default_versions()
        unsupported_versions = self.get_unsupported_versions()
        latest_default = default_versions[0]

        versions = []
        page = 1
        per_page = 100
        found_latest = False

        try:
            while True:
                response = await self.request(
                    url=self.GITHUB_API,
                    method="GET",
                    params={"per_page": per_page, "page": page},
                )

                if not response or not isinstance(response, list):
                    break

                stable_versions = [
                    release.get("tag_name")
                    for release in response
                    if release.get("tag_name")
                    and not release.get("prerelease", False)
                    and release.get("tag_name") not in unsupported_versions
                ]

                if not stable_versions:
                    break

                for version in stable_versions:
                    if version == latest_default:
                        found_latest = True
                        break

                    versions.append(version)

                if found_latest:
                    break

                page += 1

                if len(response) < per_page:
                    break

        except Exception:
            self.logger.exception(f'Error while getting "{self.name}" versions:')

        if not versions:
            return default_versions

        return versions + default_versions

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
