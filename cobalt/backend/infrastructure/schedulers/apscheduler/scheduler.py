#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.base import BaseTrigger

from application.contracts.loggers import AbstractLogger
from domain.exceptions import UnexpectedError
from infrastructure.contracts.schedulers import (
    AbstractJob,
    AbstractScheduler
)


class ApschedulerScheduler(AbstractScheduler):
    """
    Apscheduler scheduler.
    """
    scheduler: AsyncIOScheduler
    logger: AbstractLogger
    jobs: dict[str, Job]

    def __init__(
        self,
        scheduler: AsyncIOScheduler,
        logger: AbstractLogger
    ):
        self.scheduler = scheduler
        self.logger = logger
        self.jobs = {}

    def start(self) -> None:
        """
        Starts the Apscheduler.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                self.logger.info("Apscheduler started successfully.")
        except Exception as e:
            raise UnexpectedError("Failed to start Apscheduler") from e

    def shutdown(
        self,
        wait: bool = True
    ) -> None:
        """
        Stops the Apscheduler.

        Parameters:
        - wait: Whether to wait for running jobs to finish.

        Returns:
        - None.
        """
        try:
            if self.scheduler.running:
                self.scheduler.shutdown(wait=wait)
                self.logger.info("Apscheduler shutdown successfully.")
        except Exception as e:
            raise UnexpectedError("Failed to shutdown Apscheduler") from e

    def add_job(
        self,
        name: str,
        job: AbstractJob,
        trigger: Any,
        safe: bool = True
    ) -> None:
        """
        Registers a cron job in Apscheduler.

        Parameters:
        - name: Name of the cron job.
        - cron: AbstractJob object.
        - trigger: Apscheduler trigger object.
        - safe: Whether to run with concurrency protection.

        Returns:
        - None.
        """
        if not isinstance(trigger, BaseTrigger):
            self.logger.error(f"Invalid trigger type for job {name}: {type(trigger)}")
            return

        try:
            max_instances = 1 if safe else None

            created_job = self.scheduler.add_job(
                func=job.execute,
                trigger=trigger,
                id=name,
                name=name,
                max_instances=max_instances,
                coalesce=True,
                replace_existing=True,
                misfire_grace_time=None
            )

            self.jobs[name] = created_job

            self.logger.info(f"Job {name} registered with trigger: {trigger}")
        except Exception:
            self.logger.exception(f"Failed to register job {name}:")

    def remove_job(
        self,
        name: str
    ) -> None:
        """
        Unregisters the cron job from Apscheduler.

        Parameters:
        - name: Name of the cron job.

        Returns:
        - None.
        """
        try:
            job = self.jobs.pop(name, None)

            if job is None:
                return

            job.remove()

            self.logger.info(f"Job {name} unregistered.")
        except Exception:
            self.logger.exception(f"Failed to unregister job {name}:")

    def is_running(self) -> bool:
        """
        Checks if Apscheduler is running.

        Parameters:
        - None.

        Returns:
        - bool.
        """
        return self.scheduler.running