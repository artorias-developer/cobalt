#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

from application.contracts.loggers import AbstractLogger
from infrastructure.configs import (
    EnvironmentEnum,
    ApplicationConfig
)
from presentation.http.fastapi.v1.middlewares import (
    HttpErrorsMiddleware,
    HttpValidationMiddleware
)


def setup_fastapi_trusted_host_middleware(
    app: FastAPI,
    config: ApplicationConfig
) -> None:
    """
    Setups the trusted host middleware.

    Parameters:
    - app: FastAPI object.
    - config: ApplicationConfig object.

    Returns:
    - None.
    """
    allowed_hosts = [
        config.server.domain,
        f"*.{config.server.domain}",
    ]

    if config.server.environment == EnvironmentEnum.DEVELOPMENT:
        allowed_hosts.extend([
            "localhost",
            "127.0.0.1",
            "[::1]"
        ])

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts
    )

def setup_fastapi_cors_middleware(
    app: FastAPI,
    config: ApplicationConfig
) -> None:
    """
    Setups the CORS middleware.

    Parameters:
    - app: FastAPI object.
    - config: ApplicationConfig object.

    Returns:
    - None.
    """
    allowed_origins = [
        f"http://{config.server.domain}",
        f"https://{config.server.domain}",
        f"https://dashboard.{config.server.domain}",
        f"https://admin.{config.server.domain}",
    ]

    if config.server.environment == EnvironmentEnum.DEVELOPMENT:
        allowed_origins.extend([
            "http://localhost",
            "http://127.0.0.1"
        ])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["*"],
    )

def setup_fastapi_http_errors_middleware(
    app: FastAPI,
    logger: AbstractLogger
) -> None:
    """
    Setups the HTTP errors middleware.

    Parameters:
    - app: FastAPI object.
    - logger: AbstractLogger object.

    Returns:
    - None.
    """
    app.add_middleware(
        HttpErrorsMiddleware,
        logger=logger
    )

def setup_fastapi_http_validation_middleware(
    app: FastAPI,
    logger: AbstractLogger
) -> None:
    """
    Setups the HTTP validation middleware.

    Parameters:
    - app: FastAPI object.
    - logger: AbstractLogger object.

    Returns:
    - None.
    """
    handler = HttpValidationMiddleware(
        logger=logger
    )

    app.add_exception_handler(
        RequestValidationError,
        handler.dispatch
    )

def setup_fastapi_middlewares(
    app: FastAPI,
    config: ApplicationConfig,
    logger: AbstractLogger
) -> None:
    """
    Setups the application middlewares.

    Parameters:
    - app: FastAPI object.
    - config: ApplicationConfig object.
    - logger: AbstractLogger object.

    Returns:
    - None.
    """
    setup_fastapi_trusted_host_middleware(
        app=app,
        config=config
    )

    setup_fastapi_cors_middleware(
        app=app,
        config=config
    )

    setup_fastapi_http_errors_middleware(
        app=app,
        logger=logger
    )

    setup_fastapi_http_validation_middleware(
        app=app,
        logger=logger
    )
