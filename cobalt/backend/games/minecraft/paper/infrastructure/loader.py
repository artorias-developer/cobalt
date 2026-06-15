#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Optional

from domain.exceptions import UnexpectedError
from application.contracts.games import (
    AbstractLoader,
    AbstractServersService
)
from application.contracts.loggers import AbstractLogger
from infrastructure.mixins import HttpClientMixin


class PaperLoader(AbstractLoader, HttpClientMixin):
    """
    Minecraft Paper loader.
    """
    PAPER_API: str = "https://fill.papermc.io/v3"
    USER_AGENT: str = "cobalt (https://github.com/ArtoriasCode/cobalt)"

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

    @staticmethod
    def get_unsupported_versions() -> List[str]:
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
            "26.1.2",
            "26.1.1",
            "1.21.11",
            "1.21.10",
            "1.21.9",
            "1.21.8",
            "1.21.7",
            "1.21.6",
            "1.21.5",
            "1.21.4",
            "1.21.3",
            "1.21.1",
            "1.21",
            "1.20.6",
            "1.20.5",
            "1.20.4",
            "1.20.2",
            "1.20.1",
            "1.20",
            "1.19.4",
            "1.19.3",
            "1.19.2",
            "1.19.1",
            "1.19",
            "1.18.2",
            "1.18.1",
            "1.18",
            "1.17.1",
            "1.17",
            "1.16.5",
            "1.16.4",
            "1.16.3",
            "1.16.2",
            "1.16.1",
            "1.15.2",
            "1.15.1",
            "1.15",
            "1.14.4",
            "1.14.3",
            "1.14.2",
            "1.14.1",
            "1.14",
            "1.13.2",
            "1.13.1",
            "1.13",
            "1.12.2",
            "1.12.1",
            "1.12",
            "1.11.2",
            "1.10.2",
            "1.9.4",
            "1.8.8",
            "1.7.10"
        ]

    async def get_versions(self) -> List[str]:
        """
        Gets all available versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        try:
            response = await self.request(
                url=f"{self.PAPER_API}/projects/paper",
                method="GET",
                headers={"User-Agent": self.USER_AGENT}
            )

            if not response or not isinstance(response, dict):
                return self.get_default_versions()

            versions_dict = response.get("versions")

            if not versions_dict or not isinstance(versions_dict, dict):
                return self.get_default_versions()

            unsupported_versions = self.get_unsupported_versions()

            versions = [
                version
                for group in versions_dict.values()
                for version in group
                if version not in unsupported_versions
                and "-" not in version
            ]

            return versions if versions else self.get_default_versions()

        except Exception:
            self.logger.exception(f'Error while getting "{self.name}" versions:')

        return self.get_default_versions()

    async def _fetch_latest_stable_url(
        self,
        version: str
    ) -> Optional[str]:
        """
        Fetches the latest stable build download URL for the given game version.

        Parameters:
        - version: Game version string.

        Returns:
        - str: Download URL or None on failure.
        """
        try:
            response = await self.request(
                url=f"{self.PAPER_API}/projects/paper/versions/{version}/builds",
                method="GET",
                headers={"User-Agent": self.USER_AGENT}
            )

            if not response or not isinstance(response, list):
                return None

            for build in response:
                if build.get("channel") == "STABLE":
                    url = build.get("downloads", {}).get("server:default", {}).get("url")

                    if url:
                        return url

        except Exception:
            self.logger.exception(f'Error while getting "{self.name}" download URL for version {version}:')

        return None

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
        url = await self._fetch_latest_stable_url(version)

        if not url:
            self.logger.error(f'Failed to resolve stable build URL for "{self.name}" version {version}')
            raise UnexpectedError(f"Could not fetch stable Paper build for version {version}")

        return url