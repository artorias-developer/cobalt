#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any

from infrastructure.contracts.schedulers import AbstractJob


class AbstractScheduler(ABC):
    """
    Abstract scheduler for managing cron jobs.
    """

    @abstractmethod
    def start(self) -> None:
        """
        Starts the scheduler.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def shutdown(
        self,
        wait: bool = True
    ) -> None:
        """
        Stops the scheduler.

        Parameters:
        - wait: Whether to wait for running jobs to finish.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def add_job(
        self,
        name: str,
        job: AbstractJob,
        trigger: Any,
        safe: bool = True
    ) -> None:
        """
        Adds a cron job to the scheduler.

        Parameters:
        - name: Name of the cron job.
        - job: Cron job instance.
        - trigger: Trigger for the cron job.
        - safe: Whether to run with concurrency protection.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def remove_job(
        self,
        name: str
    ) -> None:
        """
        Removes a cron job from the scheduler.

        Parameters:
        - name: Name of the cron job.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def is_running(self) -> bool:
        """
        Checks if scheduler is running.

        Parameters:
        - None.

        Returns:
        - bool: True if running, False otherwise.
        """
        ...