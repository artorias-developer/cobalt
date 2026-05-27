#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Tuple, Dict, Type

from fastapi import Request, Response, FastAPI, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

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

class HttpErrorsMiddleware(BaseHTTPMiddleware):
    """
    Handles errors when processing HTTP requests.
    """
    logger: AbstractLogger

    def __init__(
        self,
        app: FastAPI,
        logger: AbstractLogger
    ):
        super().__init__(app)

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

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Dispatches a request and handles errors.

        Parameters:
        - request: Request object.
        - call_next: Callable handler.

        Returns:
        - Response: Response object.
        """
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            code, message = self.get_http_error(
                error=e
            )

            return JSONResponse(
                status_code=code,
                content={
                    "message": message
                }
            )
