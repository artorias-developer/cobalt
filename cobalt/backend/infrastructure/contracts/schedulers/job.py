#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod


class AbstractJob(ABC):
    """
    Abstract job.
    """

    @abstractmethod
    async def run(self) -> None:
        """
        Runs the cron job manually (immediately, once).

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def execute(self) -> None:
        """
        Executes the cron job logic.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...