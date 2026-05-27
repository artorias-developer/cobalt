#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .clients import create_redis_prometheus_docker_clients_container
from .databases import create_postgres_database_container
from .interceptors import setup_fastapi_interceptors
from .loggers import create_structlog_logger
from .managers import create_fastapi_managers_container
from .mappers import create_fastapi_postgres_mappers_container
from .middlewares import setup_fastapi_middlewares
from .queues import create_asyncio_queue
from .routers import setup_fastapi_routers
from .schedulers import (
    create_apscheduler_scheduler,
    create_apscheduler_jobs
)
from .dataclasses import (
    ApplicationContainer,
    ManagersContainer,
    ClientsContainer,
    MappersContainer,
    RoutersMappersContainer,
    ServicesMappersContainer,
    RepositoriesMappersContainer,
    ServicesContainer,
    DatabaseContainer,
    RepositoriesContainer,
    SchedulerJob
)
from .services import create_services_container

__all__ = [
    "create_redis_prometheus_docker_clients_container",
    "create_postgres_database_container",
    "setup_fastapi_interceptors",
    "create_structlog_logger",
    "create_fastapi_managers_container",
    "create_fastapi_postgres_mappers_container",
    "setup_fastapi_middlewares",
    "create_asyncio_queue",
    "setup_fastapi_routers",
    "create_apscheduler_scheduler",
    "create_apscheduler_jobs",
    "create_services_container",
    "ApplicationContainer",
    "ManagersContainer",
    "ClientsContainer",
    "MappersContainer",
    "RoutersMappersContainer",
    "ServicesMappersContainer",
    "RepositoriesMappersContainer",
    "ServicesContainer",
    "DatabaseContainer",
    "RepositoriesContainer",
    "SchedulerJob"
]