#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod

from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.schedulers import AbstractJob


class BaseApschedulerJob(AbstractJob):
    """
    Base job for Apscheduler.
    """
    logger: AbstractLogger

    def __init__(
        self,
        logger: AbstractLogger
    ):
        self.logger = logger

    async def run(self) -> None:
        """
        Runs the cron job manually (immediately, once).

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            await self.execute()
        except Exception:
            self.logger.exception(f"Manual execution of job failed:")

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