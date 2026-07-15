#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from application.contracts.managers import AbstractConnectionsManager
from presentation.ws.fastapi.v1.managers import ConnectionsManager


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