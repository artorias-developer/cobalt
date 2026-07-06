#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Tuple, Dict, Type

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Scope, Receive, Send

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


EXCEPTION_TO_HTTP_STATUS: Dict[Type[BaseError], int] = {
    UnexpectedError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    ValidationError: status.HTTP_400_BAD_REQUEST,
    AuthenticationError: status.HTTP_401_UNAUTHORIZED,
    PermissionsError: status.HTTP_403_FORBIDDEN,
    NotFoundError: status.HTTP_404_NOT_FOUND,
    ConflictError: status.HTTP_409_CONFLICT,
}

class HttpErrorsMiddleware:
    """
    Handles errors when processing HTTP requests.
    """
    app: ASGIApp
    logger: AbstractLogger

    def __init__(
        self,
        app: ASGIApp,
        logger: AbstractLogger
    ):
        self.app = app
        self.logger = logger

    def get_http_error(
        self,
        error: Exception
    ) -> Tuple[int, str]:
        """
        Maps exception to HTTP status code and error message.

        Parameters:
        - error: Exception to process.

        Returns:
        - Tuple: HTTP status code and error message.
        """
        if isinstance(error, BaseError):
            error_type = type(error)
            status_code = EXCEPTION_TO_HTTP_STATUS.get(error_type)

            if status_code is None:
                self.logger.warning(f"BaseError subclass {error_type.__name__} not mapped to HTTP status.")
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return status_code, str(error)

        self.logger.exception("Unhandled exception occurred:")
        return status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error"

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:
        """
        Processes an ASGI request and handles errors.

        Parameters:
        - scope: ASGI connection scope.
        - receive: Callable to receive ASGI events.
        - send: Callable to send ASGI events.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        response_started = False

        async def send_wrapper(event) -> None:
            nonlocal response_started

            if event["type"] == "http.response.start":
                response_started = True

            await send(event)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            if response_started:
                self.logger.exception("Error occurred mid-stream, response already started:")
                raise

            code, message = self.get_http_error(
                error=e
            )

            response = JSONResponse(
                status_code=code,
                content={
                    "message": message
                }
            )

            await response(scope, receive, send)