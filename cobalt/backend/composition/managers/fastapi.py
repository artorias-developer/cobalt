#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from application.contracts.managers import (
    AbstractConnectionsManager,
    AbstractEventsManager
)
from presentation.ws.fastapi.v1.managers import (
    ConnectionsManager,
    EventsManager
)
from composition.managers import create_archives_manager
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
    connections_manager: AbstractConnectionsManager
) -> AbstractEventsManager:
    """
    Creates an event manager.

    Parameters:
    - connections_manager: AbstractConnectionsManager object.

    Returns:
    - AbstractEventsManager: AbstractEventsManager object.
    """
    return EventsManager(
        connections_manager=connections_manager
    )

def create_fastapi_managers_container(
    logger: AbstractLogger
) -> ManagersContainer:
    """
    Creates the application managers container.

    Parameters:
    - logger: AbstractLogger object.

    Returns:
    - ManagersDependencies: ManagersContainer object.
    """
    connections_manager = create_fastapi_connections_manager(
        logger=logger
    )

    events_manager = create_fastapi_events_manager(
        connections_manager=connections_manager
    )

    archives_managers = create_archives_manager()

    return ManagersContainer(
        connections=connections_manager,
        events=events_manager,
        archives=archives_managers
    )