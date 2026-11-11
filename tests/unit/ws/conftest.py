#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
WebSocket test app.

Wires the real EventsManager, WsErrorsInterceptor, WsAuthMiddleware, WsEventsRouter and all event
routers. Services and the connections manager are autospec mocks.
"""

from typing import Callable, List, Optional

import pytest
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient

from domain.enums import PermissionEnum
from presentation.shared import CookieConstants
from presentation.ws.fastapi.v1.events import (
    WsLogsEvents,
    WsMetricsEvents,
    WsServersEvents
)
from presentation.ws.fastapi.v1.interceptors import WsErrorsInterceptor
from presentation.ws.fastapi.v1.managers import EventsManager
from presentation.ws.fastapi.v1.middlewares import WsAuthMiddleware
from presentation.ws.fastapi.v1.routers import WsEventsRouter

from helpers.factories import make_role_dto, make_user_dto


@pytest.fixture
def events_manager(connections_manager, i18n_manager, logger) -> EventsManager:
    manager = EventsManager(connections_manager=connections_manager)
    manager.add_interceptor(WsErrorsInterceptor(i18n_manager=i18n_manager, logger=logger))
    return manager


@pytest.fixture
def ws_client(
    events_manager,
    auth_service_mock,
    logs_service_mock,
    metrics_service_mock,
    servers_service_mock
):
    app = FastAPI()
    api_router = APIRouter(prefix="/api/v1")

    WsEventsRouter(router=api_router, events_manager=events_manager, auth_service=auth_service_mock).register()
    WsLogsEvents(
        router=api_router, events_manager=events_manager,
        logs_service=logs_service_mock, auth_service=auth_service_mock
    ).register()
    WsMetricsEvents(
        router=api_router, events_manager=events_manager,
        metrics_service=metrics_service_mock, auth_service=auth_service_mock
    ).register()
    WsServersEvents(
        router=api_router, events_manager=events_manager,
        servers_service=servers_service_mock, auth_service=auth_service_mock
    ).register()

    app.include_router(api_router)
    app.add_middleware(WsAuthMiddleware, auth_service=auth_service_mock)

    with TestClient(app, base_url="https://testserver") as client:
        yield client


@pytest.fixture
def ws_login_as(auth_service_mock) -> Callable:
    """
    Resolves the session cookie to a user with the given permissions (None = all permissions).
    """
    def _login_as(
        client: TestClient,
        permissions: Optional[List[PermissionEnum]] = None,
        user_id: int = 1
    ):
        user = make_user_dto(user_id=user_id, role=make_role_dto(permissions=permissions))
        auth_service_mock.get_session_user.return_value = user
        client.cookies.set(CookieConstants.SESSION_KEY, "ws-session")
        return user

    return _login_as

