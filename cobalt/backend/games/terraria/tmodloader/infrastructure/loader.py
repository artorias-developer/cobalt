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


class TModLoaderLoader(AbstractLoader, HttpClientMixin):
    """
    Terraria TModLoader loader.
    """
    GITHUB_API = "https://api.github.com/repos/tModLoader/tModLoader/releases"
    DOWNLOAD_LINK = "https://github.com/tModLoader/tModLoader/releases/download/{version}/tModLoader.zip"

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
            "v2022.09.47.40",
            "v2022.09.47.39",
            "v2022.03.35.11",
            "v2022.03.35.6",
            "v0.11.8.9",
            "v0.11.8.8",
            "v0.11.8.7",
            "v0.11.8.6",
            "v0.11.8.5",
            "v0.11.8.4",
            "v0.11.8.3",
            "v0.11.8.2",
            "v0.11.8.1",
            "v0.11.8",
            "v0.11.7.8",
            "v0.11.7.7",
            "v0.11.7.6",
            "v0.11.7.5",
            "v0.11.7.4",
            "v0.11.7.3",
            "v0.11.7.2",
            "v0.11.7.1",
            "v0.11.7",
            "v0.11.6.2",
            "v0.11.6.1",
            "v0.11.5",
            "v0.11.4",
            "v0.11.3",
            "v0.11.2.2",
            "v0.11.2.1",
            "v0.11.2",
            "v0.11.1",
            "v0.11",
            "v0.10.1.5"
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
            "v2026.03.3.0",
            "v2026.02.3.2",
            "v2026.02.3.1",
            "v2026.02.3.0",
            "v2026.01.3.3",
            "v2026.01.3.2",
            "v2026.01.3.1",
            "v2025.12.3.1",
            "v2025.12.3.0",
            "v2025.11.3.3",
            "v2025.11.3.2",
            "v2025.11.3.1",
            "v2025.11.3.0",
            "v2025.10.3.1",
            "v2025.09.3.4",
            "v2025.09.3.3",
            "v2025.09.3.2",
            "v2025.09.3.1",
            "v2025.09.3.0",
            "v2025.08.3.1",
            "v2025.08.3.0",
            "v2025.07.3.1",
            "v2025.07.3.0",
            "v2025.06.3.0",
            "v2025.05.3.0",
            "v2025.04.3.0",
            "v2025.03.3.1",
            "v2025.03.3.0",
            "v2025.02.3.3",
            "v2025.02.3.2",
            "v2025.02.3.1",
            "v2025.02.3.0",
            "v2025.01.3.1",
            "v2025.01.3.0",
            "v2024.12.3.1",
            "v2024.12.3.0",
            "v2024.11.3.2",
            "v2024.11.3.0",
            "v2024.10.3.0",
            "v2024.09.3.0",
            "v2024.08.3.1",
            "v2024.07.3.2",
            "v2024.06.3.1",
            "v2024.06.3.0",
            "v2024.05.3.3",
            "v2024.05.3.1",
            "v2024.05.3.0",
            "v2024.04.3.2",
            "v2024.04.3.1",
            "v2024.04.3.0",
            "v2024.03.3.4",
            "v2024.03.3.3",
            "v2024.03.3.2",
            "v2024.03.3.1",
            "v2024.03.3.0",
            "v2024.02.3.0",
            "v2024.01.3.0",
            "v2023.12.3.1",
            "v2023.12.3.0",
            "v2023.11.3.3",
            "v2023.11.3.1",
            "v2023.11.3.0",
            "v2023.10.3.0",
            "v2023.09.3.3",
            "v2023.09.3.2",
            "v2023.09.3.0",
            "v2023.08.3.4",
            "v2023.08.3.3",
            "v2023.08.3.2",
            "v2023.08.3.1",
            "v2023.08.3.0",
            "v2023.06.25.36",
            "v2023.06.25.35",
            "v2023.06.25.34",
            "v2023.06.25.33",
            "v2023.06.25.32",
            "v2023.06.25.31",
            "v2023.06.25.30",
            "v2023.06.25.29",
            "v2023.06.25.28",
            "v2023.06.25.27",
            "v2023.06.25.26",
            "v2022.09.47.82",
            "v2022.09.47.75",
            "v2022.09.47.57",
            "v2022.09.47.55",
            "v2022.09.47.52",
            "v2022.09.47.50",
            "v2022.09.47.49",
            "v2022.09.47.48",
            "v2022.09.47.47",
            "v2022.09.47.46",
            "v2022.09.47.45",
            "v2022.09.47.44",
            "v2022.09.47.42",
            "v2022.09.47.41",
            "v2022.09.47.38",
            "v2022.09.47.37",
            "v2022.09.47.36",
            "v2022.09.47.35",
            "v2022.09.47.34",
            "v2022.09.47.33",
            "v2022.09.47.32",
            "v2022.09.47.31",
            "v2022.09.47.30",
            "v2022.09.47.29",
            "v2022.09.47.28",
            "v2022.09.47.27",
            "v2022.09.47.26",
            "v2022.09.47.24",
            "v2022.09.47.23",
            "v2022.09.47.21",
            "v2022.09.47.20",
            "v2022.09.47.18",
            "v2022.09.47.17",
            "v2022.09.47.16",
            "v2022.09.47.15",
            "v2022.09.47.14",
            "v2022.09.47.13",
            "v2022.09.47.12",
            "v2022.09.47.11",
            "v2022.09.47.10",
            "v2022.09.47.9",
            "v2022.09.47.8",
            "v2022.09.47.7",
            "v2022.09.47.6",
            "v2022.09.47.5",
            "v2022.09.47.4",
            "v2022.09.47.3",
            "v2022.09.47.2",
            "v2022.09.47.1",
            "v2022.08.54.6",
            "v2022.08.54.5",
            "v2022.08.54.4",
            "v2022.08.54.3",
            "v2022.08.54.2",
            "v2022.08.54.1",
            "v2022.07.58.9",
            "v2022.07.58.8",
            "v2022.07.58.7",
            "v2022.07.58.6",
            "v2022.07.58.5",
            "v2022.07.58.4",
            "v2022.07.58.3",
            "v2022.07.58.2",
            "v2022.07.58.1",
            "v2022.06.96.4",
            "v2022.06.96.3",
            "v2022.06.96.2",
            "v2022.06.96.1",
            "v2022.05.103.34",
            "v2022.05.103.33",
            "v2022.05.103.32",
            "v2022.05.103.31",
            "v2022.05.103.30",
            "v2022.05.103.29",
            "v2022.05.103.28",
            "v2022.05.103.27",
            "v2022.05.103.26",
            "v2022.05.103.25",
            "v2022.05.103.24",
            "v2022.05.103.22",
            "v2022.05.103.21",
            "v2022.05.103.20",
            "v2022.05.103.18",
            "v2022.05.103.17",
            "v2022.05.103.16",
            "v2022.05.103.15",
            "v2022.05.103.14",
            "v2022.05.103.12",
            "v2022.05.103.9",
            "v2022.05.103.8",
            "v2022.05.103.7",
            "v2022.05.103.6",
            "v2022.05.103.11",
            "v2022.05.103.10",
            "v2022.05.103.5",
            "v2022.05.103.4",
            "v2022.05.103.3",
            "v2022.05.103.2",
            "v2022.04.62.6",
            "v2022.04.62.5",
            "v2022.04.62.4",
            "v2022.04.62.1"
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
