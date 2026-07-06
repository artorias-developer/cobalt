#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

from application.contracts.loggers import AbstractLogger
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import AbstractAuthService
from infrastructure.configs import (
    EnvironmentEnum,
    ApplicationConfig
)
from presentation.http.fastapi.v1.middlewares import (
    HttpErrorsMiddleware,
    HttpAuthMiddleware,
    HttpLocaleMiddleware,
    HttpValidationMiddleware
)
from presentation.ws.fastapi.v1.middlewares import (
    WsAuthMiddleware,
    WsLocaleMiddleware
)
from composition.dataclasses import (
    ManagersContainer,
    ServicesContainer
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
            "[::1]",
            "*.ngrok-free.app"
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
            "http://127.0.0.1",
            "https://*.ngrok-free.app"
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

def setup_fastapi_http_locale_middleware(
    app: FastAPI,
    i18n_manager: AbstractI18nManager
) -> None:
    """
    Setups the HTTP locale middleware.

    Parameters:
    - app: FastAPI object.
    - i18n_manager: AbstractI18nManager object.

    Returns:
    - None.
    """
    app.add_middleware(
        HttpLocaleMiddleware,
        i18n_manager=i18n_manager
    )

def setup_fastapi_http_auth_middleware(
    app: FastAPI,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP auth middleware.

    Parameters:
    - app: FastAPI object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    app.add_middleware(
        HttpAuthMiddleware,
        auth_service=auth_service
    )

def setup_fastapi_http_validation_middleware(
    app: FastAPI,
    i18n_manager: AbstractI18nManager,
    logger: AbstractLogger
) -> None:
    """
    Setups the HTTP validation middleware.

    Parameters:
    - app: FastAPI object.
    - i18n_manager: AbstractI18nManager object.
    - logger: AbstractLogger object.

    Returns:
    - None.
    """
    handler = HttpValidationMiddleware(
        i18n_manager=i18n_manager,
        logger=logger
    )

    app.add_exception_handler(
        RequestValidationError,
        handler.dispatch
    )

def setup_fastapi_ws_locale_middleware(
    app: FastAPI,
    i18n_manager: AbstractI18nManager
) -> None:
    """
    Setups the WebSocket locale middleware.

    Parameters:
    - app: FastAPI object.
    - i18n_manager: AbstractI18nManager object.

    Returns:
    - None.
    """
    app.add_middleware(
        WsLocaleMiddleware,
        i18n_manager=i18n_manager
    )

def setup_fastapi_ws_auth_middleware(
    app: FastAPI,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the WebSocket auth middleware.

    Parameters:
    - app: FastAPI object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    app.add_middleware(
        WsAuthMiddleware,
        auth_service=auth_service
    )

def setup_fastapi_middlewares(
    app: FastAPI,
    config: ApplicationConfig,
    services: ServicesContainer,
    managers: ManagersContainer,
    logger: AbstractLogger
) -> None:
    """
    Setups the application middlewares.

    Parameters:
    - app: FastAPI object.
    - config: ApplicationConfig object.
    - services: ServicesContainer object.
    - managers: ManagersContainer object.
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

    setup_fastapi_http_locale_middleware(
        app=app,
        i18n_manager=managers.i18n
    )

    setup_fastapi_http_auth_middleware(
        app=app,
        auth_service=services.auth
    )

    setup_fastapi_http_validation_middleware(
        app=app,
        i18n_manager=managers.i18n,
        logger=logger
    )

    setup_fastapi_ws_locale_middleware(
        app=app,
        i18n_manager=managers.i18n
    )

    setup_fastapi_ws_auth_middleware(
        app=app,
        auth_service=services.auth
    )

