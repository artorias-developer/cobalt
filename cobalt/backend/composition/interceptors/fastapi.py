#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from presentation.ws.fastapi.v1.interceptors import WsErrorsInterceptor
from composition.dataclasses import ManagersContainer


def setup_fastapi_ws_errors_interceptor(
    managers: ManagersContainer,
    logger: AbstractLogger
) -> None:
    """
    Setups the WebSocket errors interceptor.

    Parameters:
    - managers: ManagersContainer object.
    - logger: AbstractLogger object.

    Returns:
    - None.
    """
    errors_interceptor = WsErrorsInterceptor(
        logger=logger
    )

    managers.events.add_interceptor(
        errors_interceptor
    )

def setup_fastapi_interceptors(
    managers: ManagersContainer,
    logger: AbstractLogger
) -> None:
    """
    Setups the application interceptors.

    Parameters:
    - managers: ManagersContainer object.
    - logger: AbstractLogger object.

    Returns:
    - None.
    """
    setup_fastapi_ws_errors_interceptor(
        managers=managers,
        logger=logger
    )
