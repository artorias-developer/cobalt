#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Callable, Tuple, Dict, Type, Any

from fastapi import WebSocket, status
from pydantic import ValidationError as PydanticValidationError
from starlette.websockets import WebSocketState

from domain.exceptions import (
    BaseError,
    UnexpectedError,
    ValidationError,
    AuthenticationError,
    PermissionsError,
    NotFoundError,
    ConflictError
)
from application.contracts.loggers import AbstractLogger
from application.contracts.interceptors import AbstractInterceptor
from presentation.ws.shared import WebSocketStatusCodesEnum


EXCEPTION_TO_WS_STATUS: Dict[Type[BaseError], int] = {
    UnexpectedError: WebSocketStatusCodesEnum.WS_1011_INTERNAL_SERVER_ERROR,
    ValidationError: WebSocketStatusCodesEnum.WS_4400_BAD_REQUEST,
    AuthenticationError: WebSocketStatusCodesEnum.WS_4401_UNAUTHORIZED,
    PermissionsError: WebSocketStatusCodesEnum.WS_4403_FORBIDDEN,
    NotFoundError: WebSocketStatusCodesEnum.WS_4404_NOT_FOUND,
    ConflictError: WebSocketStatusCodesEnum.WS_4409_CONFLICT
}

class WsErrorsInterceptor(AbstractInterceptor):
    """
    Handles errors when processing WebSockets events.
    """
    logger: AbstractLogger

    def __init__(
        self,
        logger: AbstractLogger
    ):
        self.logger = logger

    def _get_ws_error(
        self,
        error: Exception
    ) -> Tuple[int, str]:
        """
        Maps exception to WS status code and error message.

        Parameters:
        - error: Exception to process.

        Returns:
        - Tuple: WS status code and error message.
        """
        if isinstance(error, BaseError):
            error_type = type(error)
            status_code = EXCEPTION_TO_WS_STATUS.get(error_type)

            if status_code is None:
                self.logger.warning(f"BaseError subclass {error_type.__name__} not mapped to WS status.")
                status_code = status.WS_1011_INTERNAL_ERROR

            return status_code, str(error)

        elif isinstance(error, PydanticValidationError):
            status_code = WebSocketStatusCodesEnum.WS_4400_BAD_REQUEST

            return status_code, str(error)

        self.logger.exception("Unhandled exception occurred:")
        return status.WS_1011_INTERNAL_ERROR, "Internal server error"

    async def dispatch(
        self,
        call_next: Callable,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Dispatches a request and handles errors.

        Parameters:
        - call_next: Async callable that processes the WebSockets connection.
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        try:
            await call_next()
        except Exception as e:
            code, message = self._get_ws_error(
                error=e
            )

            websocket: WebSocket = kwargs.get("websocket")

            if not websocket:
                return

            if websocket.client_state != WebSocketState.CONNECTED:
                return

            await websocket.send_json({
                "type": "error",
                "code": code,
                "data": message
            })