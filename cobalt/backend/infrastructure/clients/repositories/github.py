#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Optional

from application.contracts.clients import (
    AbstractHttpClient,
    AbstractRepositoriesClient
)
from application.contracts.loggers import AbstractLogger


class GithubClient(AbstractRepositoriesClient):
    """
    Client for GitHub repositories.
    """
    GITHUB_API = "https://api.github.com/repos/{repository}"

    http_client: AbstractHttpClient

    def __init__(
        self,
        http_client: AbstractHttpClient,
        logger: AbstractLogger
    ):
        self.http_client = http_client
        self.logger = logger

    async def get_all_versions(
        self,
        repository: str,
        pre_release: bool = False,
        per_page: int = 100,
        stop_on_version: Optional[str] = None
    ) -> List[str]:
        """
        Gets all release versions from a GitHub repository.

        Parameters:
        - repository: Repository URL.
        - pre_release: Whether to include prerelease versions.
        - per_page: Number of releases to fetch per page.
        - stop_on_version: Stop fetching once this version tag is reached.

        Returns:
        - List: List of versions.
        """
        url = self.GITHUB_API.format(
            repository=repository
        )

        versions = []
        page = 1
        found_stop_version = False

        try:
            while True:
                response = await self.http_client.request(
                    url=f"{url}/releases",
                    method="GET",
                    params={"per_page": per_page, "page": page},
                )

                if not response or not isinstance(response, list):
                    break

                for release in response:
                    tag_name = release.get("tag_name")

                    if not tag_name:
                        continue

                    if not pre_release and release.get("prerelease", False):
                        continue

                    if tag_name == stop_on_version:
                        found_stop_version = True
                        break

                    versions.append(tag_name)

                if found_stop_version:
                    break

                if len(response) < per_page:
                    break

                page += 1

        except Exception:
            self.logger.exception(f'Error while getting "{repository}" release versions:')

        return versions