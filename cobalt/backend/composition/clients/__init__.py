#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from infrastructure.configs import ApplicationConfig
from composition.dataclasses import (
    ClientsContainer,
    ManagersContainer
)

from .caches import create_redis_client
from .containers import create_docker_client
from .metrics import create_prometheus_client

__all__ = [
    "create_redis_prometheus_docker_clients_container"
]


def create_redis_prometheus_docker_clients_container(
    config: ApplicationConfig,
    managers: ManagersContainer,
    logger: AbstractLogger
) -> ClientsContainer:
    """
    Creates the application clients container.

    Parameters:
    - config: ApplicationConfig object.
    - managers: ServicesContainer object.
    - logger: AbstractLogger object.

    Returns:
    - ClientsContainer: ClientsContainer object.
    """
    caches_client = create_redis_client(
        config=config,
        i18n_manager=managers.i18n,
        logger=logger
    )

    metrics_client = create_prometheus_client(
        config=config,
        logger=logger
    )

    containers_client = create_docker_client(
        i18n_manager=managers.i18n
    )

    return ClientsContainer(
        caches=caches_client,
        metrics=metrics_client,
        containers=containers_client
    )