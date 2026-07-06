#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timezone
from typing import List, Dict

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from application.contracts.games import AbstractGameModule
from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.schedulers import AbstractScheduler
from infrastructure.schedulers.apscheduler import ApschedulerScheduler
from infrastructure.schedulers.apscheduler.jobs import (
    HostCpuMetricsStreamingJob,
    HostRamMetricsStreamingJob,
    ServersCpuMetricsStreamingJob,
    ServersRamMetricsStreamingJob,
    LoaderVersionsCheckerJob,
    FailedServersCheckerJob,
    StartupServersCheckerJob
)
from composition.dataclasses import (
    ServicesContainer,
    ManagersContainer,
    SchedulerJob
)


def create_apscheduler_jobs(
    services: ServicesContainer,
    managers: ManagersContainer,
    logger: AbstractLogger,
    game_modules: Dict[str, AbstractGameModule]
) -> List[SchedulerJob]:
    """
    Creates apscheduler jobs.

    Parameters:
    - services: ServicesContainer object.
    - managers: ManagersContainer object.
    - logger: AbstractLogger object.
    - game_modules: Game modules dictionary.

    Returns:
    - List: List of apscheduler jobs.
    """
    return [
        SchedulerJob(
            name="HostCpuMetricsStreamingJob",
            instance=HostCpuMetricsStreamingJob(
                metrics_service=services.metrics,
                connections_manager=managers.connections,
                logger=logger
            ),
            trigger=IntervalTrigger(
                seconds=3
            )
        ),
        SchedulerJob(
            name="HostRamMetricsStreamingJob",
            instance=HostRamMetricsStreamingJob(
                metrics_service=services.metrics,
                connections_manager=managers.connections,
                logger=logger
            ),
            trigger=IntervalTrigger(
                seconds=3
            )
        ),
        SchedulerJob(
            name="ServersCpuMetricsStreamingJob",
            instance=ServersCpuMetricsStreamingJob(
                metrics_service=services.metrics,
                connections_manager=managers.connections,
                logger=logger
            ),
            trigger=IntervalTrigger(
                seconds=3
            )
        ),
        SchedulerJob(
            name="ServersRamMetricsStreamingJob",
            instance=ServersRamMetricsStreamingJob(
                metrics_service=services.metrics,
                connections_manager=managers.connections,
                logger=logger
            ),
            trigger=IntervalTrigger(
                seconds=3
            )
        ),
        SchedulerJob(
            name="FailedServersCheckerJob",
            instance=FailedServersCheckerJob(
                servers_service=services.servers,
                logger=logger
            ),
            trigger=CronTrigger(
                hour="*/3"
            )
        ),
        SchedulerJob(
            name="StartupServersCheckerJob",
            instance=StartupServersCheckerJob(
                servers_service=services.servers,
                logger=logger
            ),
            trigger=DateTrigger(
                run_date=datetime.now(timezone.utc)
            )
        ),
        SchedulerJob(
            name="LoaderVersionsCheckerJob",
            instance=LoaderVersionsCheckerJob(
                game_modules=game_modules,
                logger=logger
            ),
            trigger=CronTrigger(
                hour="*/5"
            )
        )
    ]

def create_apscheduler_scheduler(
    logger: AbstractLogger
) -> AbstractScheduler:
    """
    Creates the Apscheduler scheduler.

    Parameters:
    - logger: AbstractLogger object.

    Returns:
    - AbstractScheduler: AbstractScheduler object.
    """
    apscheduler_client = AsyncIOScheduler()

    return ApschedulerScheduler(
        scheduler=apscheduler_client,
        logger=logger
    )
