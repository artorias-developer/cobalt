#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Optional

from application.contracts.loggers import AbstractLogger
from infrastructure.mixins.clients.http import HttpClientMixin


class GithubClientMixin(HttpClientMixin):
    """
    Mixin for GitHub API client.
    """
    GITHUB_API = "https://api.github.com/repos/{repository}"

    def __init__(
        self,
        logger: AbstractLogger,
        timeout: float = 60.0
    ):
        super().__init__(logger, timeout)

    async def get_repository_release_versions(
        self,
        repository: str,
        prerelease: bool = False,
        per_page: int = 100,
        stop_on_version: Optional[str] = None
    ) -> List[str]:
        """
        Gets release version tags for a GitHub repository.

        Parameters:
        - repository: Repository in "owner/repository" format.
        - prerelease: Whether to include prerelease versions.
        - per_page: Number of releases to fetch per page.
        - stop_on_version: Stop fetching once this version tag is reached.

        Returns:
        - List: List of release version tags.
        """
        url = self.GITHUB_API.format(
            repository=repository
        )

        versions = []
        page = 1
        found_stop_version = False

        try:
            while True:
                response = await self.request(
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

                    if not prerelease and release.get("prerelease", False):
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