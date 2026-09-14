#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List, Optional


class AbstractRepositoriesClient(ABC):
    """
    Abstract repositories client.
    """

    @abstractmethod
    async def get_all_versions(
        self,
        repository: str,
        pre_release: bool = False,
        per_page: int = 100,
        stop_on_version: Optional[str] = None
    ) -> List[str]:
        """
        Gets all release versions from a repository.

        Parameters:
        - repository: Repository URL.
        - pre_release: Whether to include prerelease versions.
        - per_page: Number of releases to fetch per page.
        - stop_on_version: Stop fetching once this version tag is reached.

        Returns:
        - List: List of versions.
        """
        ...