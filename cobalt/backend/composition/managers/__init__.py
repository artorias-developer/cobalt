#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from infrastructure.configs import ApplicationConfig
from composition.dataclasses import ManagersContainer

from .archives import create_archives_manager
from .connections import create_fastapi_connections_manager
from .events import create_fastapi_events_manager
from .i18n import create_i18n_manager

__all__ = [
    "create_fastapi_managers_container"
]


def create_fastapi_managers_container(
    config: ApplicationConfig,
    logger: AbstractLogger
) -> ManagersContainer:
    """
    Creates the application managers container.

    Parameters:
    - logger: AbstractLogger object.

    Returns:
    - ManagersDependencies: ManagersContainer object.
    """
    i18n_manager = create_i18n_manager(
        config=config
    )

    connections_manager = create_fastapi_connections_manager(
        logger=logger
    )

    events_manager = create_fastapi_events_manager(
        connections_manager=connections_manager,
        i18n_manager=i18n_manager
    )

    archives_managers = create_archives_manager()

    return ManagersContainer(
        i18n=i18n_manager,
        connections=connections_manager,
        events=events_manager,
        archives=archives_managers
    )