#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
Builds a lightweight FastAPI app for router tests.

Uses the real routers, router mappers, error/auth middlewares and validation handler,
while every service is replaced with a mock. No database, cache or Docker is required.
"""

from typing import Callable, Iterable

from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient

from application.contracts.loggers import AbstractLogger
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import AbstractAuthService
from presentation.http.fastapi.v1.middlewares import (
    HttpErrorsMiddleware,
    HttpAuthMiddleware,
    HttpValidationMiddleware
)


API_PREFIX = "/api/v1"

RouterFactory = Callable[[APIRouter], object]


def build_test_client(
    router_factories: Iterable[RouterFactory],
    auth_service: AbstractAuthService,
    i18n_manager: AbstractI18nManager,
    logger: AbstractLogger
) -> TestClient:
    """
    Creates a TestClient with the given routers registered under /api/v1.

    Parameters:
    - router_factories: Callables that receive the API router and return a router instance with `register()`.
    - auth_service: Mocked auth service used by the auth middleware.
    - i18n_manager: Mocked i18n manager.
    - logger: Mocked logger.

    Returns:
    - TestClient: Configured test client.
    """
    app = FastAPI()
    api_router = APIRouter(prefix=API_PREFIX)

    for factory in router_factories:
        factory(api_router).register()

    app.include_router(api_router)

    validation_handler = HttpValidationMiddleware(
        i18n_manager=i18n_manager,
        logger=logger
    )

    app.add_exception_handler(RequestValidationError, validation_handler.dispatch)

    # Same order as composition.middlewares: auth is added first, errors wraps it.
    app.add_middleware(HttpAuthMiddleware, auth_service=auth_service)
    app.add_middleware(HttpErrorsMiddleware, i18n_manager=i18n_manager, logger=logger)

    return TestClient(app, base_url="https://testserver")
