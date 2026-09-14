#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from infrastructure.configs import ApplicationConfig
from composition.dataclasses import ClientsContainer

from .caches import create_redis_client
from .containers import create_docker_client
from .metrics import create_prometheus_client
from .http import create_aiohttp_client
from .repositories import create_github_client

__all__ = [
    "create_clients_container"
]


def create_clients_container(
    config: ApplicationConfig,
    logger: AbstractLogger
) -> ClientsContainer:
    """
    Creates the application clients container.

    Parameters:
    - config: ApplicationConfig object.
    - logger: AbstractLogger object.

    Returns:
    - ClientsContainer: ClientsContainer object.
    """
    http_client = create_aiohttp_client(
        logger=logger
    )

    github_client = create_github_client(
        http_client=http_client,
        logger=logger
    )

    cache_client = create_redis_client(
        config=config,
        logger=logger
    )

    metrics_client = create_prometheus_client(
        config=config,
        http_client=http_client,
        logger=logger
    )

    containers_client = create_docker_client()

    return ClientsContainer(
        caches=cache_client,
        metrics=metrics_client,
        containers=containers_client,
        http=http_client,
        github=github_client
    )