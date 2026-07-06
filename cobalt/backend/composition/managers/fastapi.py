#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from application.contracts.managers import (
    AbstractConnectionsManager,
    AbstractEventsManager, AbstractI18nManager
)
from infrastructure.configs import ApplicationConfig
from presentation.ws.fastapi.v1.managers import (
    ConnectionsManager,
    EventsManager
)
from composition.managers.archives import create_archives_manager
from composition.managers.i18n import create_i18n_manager
from composition.dataclasses import ManagersContainer


def create_fastapi_connections_manager(
    logger: AbstractLogger
) -> AbstractConnectionsManager:
    """
    Creates a connection manager.

    Parameters:
    - logger: AbstractLogger object.

    Returns:
    - AbstractConnectionsManager: AbstractConnectionsManager object.
    """
    return ConnectionsManager(
        logger=logger
    )

def create_fastapi_events_manager(
    connections_manager: AbstractConnectionsManager,
    i18n_manager: AbstractI18nManager
) -> AbstractEventsManager:
    """
    Creates an event manager.

    Parameters:
    - connections_manager: AbstractConnectionsManager object.
    - i18n_manager: AbstractI18nManager object.

    Returns:
    - AbstractEventsManager: AbstractEventsManager object.
    """
    return EventsManager(
        connections_manager=connections_manager,
        i18n_manager=i18n_manager
    )

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