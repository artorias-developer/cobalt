#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict

from fastapi import FastAPI, APIRouter

from application.contracts.games import AbstractGameModule
from infrastructure.configs import ApplicationConfig
from composition.dataclasses import ApplicationContainer
from composition.managers import create_fastapi_managers_container
from composition.clients import create_clients_container
from composition.mappers import create_fastapi_postgres_mappers_container
from composition.databases import create_postgres_database_container
from composition.services import create_services_container
from composition.middlewares import setup_fastapi_middlewares
from composition.interceptors import setup_fastapi_interceptors
from composition.routers import setup_fastapi_routers
from composition.hashers import create_bcrypt_hasher
from composition.loggers import create_structlog_logger
from composition.queues import create_asyncio_queue
from composition.schedulers import (
    create_apscheduler_scheduler,
    create_apscheduler_jobs
)


def setup_fastapi_ioc_container(
    config: ApplicationConfig,
    game_modules: Dict[str, AbstractGameModule]
) -> ApplicationContainer:
    """
    Builds the application's dependency graph.

    Parameters:
    - config: Application configuration.
    - game_modules: Dictionary of initialized game modules.

    Returns:
    - ApplicationContainer: ApplicationContainer object.
    """
    logger = create_structlog_logger(
        config=config
    )

    hasher = create_bcrypt_hasher(
        config=config,
        logger=logger
    )

    scheduler = create_apscheduler_scheduler(
        logger=logger
    )

    queue = create_asyncio_queue(
        logger=logger
    )

    managers_container = create_fastapi_managers_container(
        config=config,
        logger=logger
    )

    clients_container = create_clients_container(
        config=config,
        managers=managers_container,
        logger=logger
    )

    mappers_container = create_fastapi_postgres_mappers_container()

    database_container = create_postgres_database_container(
        config=config,
        managers=managers_container,
        mappers=mappers_container,
        logger=logger
    )

    services_container = create_services_container(
        config=config,
        managers=managers_container,
        clients=clients_container,
        mappers=mappers_container,
        database=database_container,
        logger=logger,
        hasher=hasher,
        queue=queue,
        game_modules=game_modules
    )

    jobs = create_apscheduler_jobs(
        services=services_container,
        managers=managers_container,
        logger=logger,
        game_modules=game_modules
    )

    return ApplicationContainer(
        logger=logger,
        hasher=hasher,
        scheduler=scheduler,
        queue=queue,
        clients=clients_container,
        managers=managers_container,
        mappers=mappers_container,
        services=services_container,
        database=database_container,
        jobs=jobs
    )


def setup_fastapi_app(
    app: FastAPI,
    router: APIRouter,
    config: ApplicationConfig,
    container: ApplicationContainer
) -> None:
    """
    Wires the FastAPI app and router using an already-built dependency container.

    Parameters:
    - app: FastAPI application instance.
    - router: FastAPI router instance.
    - config: Application configuration.
    - container: Already assembled ApplicationContainer.

    Returns:
    - None.
    """
    setup_fastapi_interceptors(
        managers=container.managers,
        logger=container.logger
    )

    setup_fastapi_middlewares(
        app=app,
        config=config,
        managers=container.managers,
        services=container.services,
        logger=container.logger
    )

    setup_fastapi_routers(
        router=router,
        managers=container.managers,
        mappers=container.mappers,
        services=container.services
    )