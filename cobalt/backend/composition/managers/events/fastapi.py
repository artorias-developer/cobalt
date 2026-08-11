#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.managers import (
    AbstractConnectionsManager,
    AbstractEventsManager
)
from presentation.ws.fastapi.v1.managers import EventsManager


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
