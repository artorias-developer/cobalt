#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter

from application.contracts.managers import AbstractEventsManager
from application.contracts.services import (
    AbstractAuthService,
    AbstractGamesService,
    AbstractAttributesService,
    AbstractRolesService,
    AbstractSettingsService,
    AbstractUsersService,
    AbstractLogsService,
    AbstractMetricsService,
    AbstractServersService,
    AbstractFilesService
)
from presentation.contracts.http.mappers import (
    AbstractAuthRouterMapper,
    AbstractGamesRouterMapper,
    AbstractAttributesRouterMapper,
    AbstractRolesRouterMapper,
    AbstractSettingsRouterMapper,
    AbstractUsersRouterMapper,
    AbstractLogsRouterMapper,
    AbstractMetricsRouterMapper,
    AbstractServersRouterMapper,
    AbstractFilesRouterMapper
)
from presentation.http.fastapi.v1.routers import (
    HttpAuthRouter,
    HttpGamesRouter,
    HttpAttributesRouter,
    HttpRolesRouter,
    HttpSettingsRouter,
    HttpUsersRouter,
    HttpLogsRouter,
    HttpMetricsRouter,
    HttpServersRouter,
    HttpFilesRouter
)
from presentation.ws.fastapi.v1.routers import (
    WsEventsRouter
)
from presentation.ws.fastapi.v1.events import (
    WsMetricsEvents,
    WsLogsEvents,
    WsServersEvents
)
from composition.dataclasses import (
    ManagersContainer,
    ServicesContainer,
    MappersContainer
)


def setup_fastapi_http_auth_router(
    router: APIRouter,
    auth_service: AbstractAuthService,
    auth_mapper: AbstractAuthRouterMapper
) -> None:
    """
    Setups the HTTP auth router.

    Parameters:
    - router: APIRouter object.
    - auth_service: AbstractAuthService object.
    - auth_mapper: AbstractAuthRouterMapper object.

    Returns:
    - None.
    """
    http_auth_router = HttpAuthRouter(
        router=router,
        auth_service=auth_service,
        auth_mapper=auth_mapper
    )

    http_auth_router.register()

def setup_fastapi_http_attributes_router(
    router: APIRouter,
    attributes_service: AbstractAttributesService,
    attributes_mapper: AbstractAttributesRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP attributes router.

    Parameters:
    - router: APIRouter object.
    - attributes_service: AbstractAttributesService object.
    - attributes_mapper: AbstractAttributesRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_attributes_router = HttpAttributesRouter(
        router=router,
        attributes_service=attributes_service,
        attributes_mapper=attributes_mapper,
        auth_service=auth_service
    )

    http_attributes_router.register()

def setup_fastapi_http_roles_router(
    router: APIRouter,
    roles_service: AbstractRolesService,
    roles_mapper: AbstractRolesRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP roles router.

    Parameters:
    - router: APIRouter object.
    - roles_service: AbstractRolesService object.
    - roles_mapper: AbstractRolesRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_roles_router = HttpRolesRouter(
        router=router,
        roles_service=roles_service,
        roles_mapper=roles_mapper,
        auth_service=auth_service
    )

    http_roles_router.register()

def setup_fastapi_http_settings_router(
    router: APIRouter,
    settings_service: AbstractSettingsService,
    settings_mapper: AbstractSettingsRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP settings router.

    Parameters:
    - router: APIRouter object.
    - settings_service: AbstractSettingsService object.
    - settings_mapper: AbstractSettingsRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_settings_router = HttpSettingsRouter(
        router=router,
        settings_service=settings_service,
        settings_mapper=settings_mapper,
        auth_service=auth_service
    )

    http_settings_router.register()

def setup_fastapi_http_users_router(
    router: APIRouter,
    users_service: AbstractUsersService,
    users_mapper: AbstractUsersRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP users router.

    Parameters:
    - router: APIRouter object.
    - users_service: AbstractUsersService object.
    - users_mapper: AbstractUsersRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_users_router = HttpUsersRouter(
        router=router,
        users_service=users_service,
        users_mapper=users_mapper,
        auth_service=auth_service
    )

    http_users_router.register()

def setup_fastapi_http_logs_router(
    router: APIRouter,
    logs_service: AbstractLogsService,
    logs_mapper: AbstractLogsRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP logs router.

    Parameters:
    - router: APIRouter object.
    - logs_service: AbstractLogsService object.
    - logs_mapper: AbstractLogsRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_logs_router = HttpLogsRouter(
        router=router,
        logs_service=logs_service,
        logs_mapper=logs_mapper,
        auth_service=auth_service
    )

    http_logs_router.register()

def setup_fastapi_http_metrics_router(
    router: APIRouter,
    metrics_service: AbstractMetricsService,
    metrics_mapper: AbstractMetricsRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP metrics router.

    Parameters:
    - router: APIRouter object.
    - metrics_service: AbstractMetricsService object.
    - metrics_mapper: AbstractMetricsRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_metrics_router = HttpMetricsRouter(
        router=router,
        metrics_service=metrics_service,
        metrics_mapper=metrics_mapper,
        auth_service=auth_service
    )

    http_metrics_router.register()

def setup_fastapi_http_servers_router(
    router: APIRouter,
    servers_service: AbstractServersService,
    servers_mapper: AbstractServersRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP servers router.

    Parameters:
    - router: APIRouter object.
    - servers_service: AbstractServersService object.
    - servers_mapper: AbstractServersRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_servers_router = HttpServersRouter(
        router=router,
        servers_service=servers_service,
        servers_mapper=servers_mapper,
        auth_service=auth_service
    )

    http_servers_router.register()

def setup_fastapi_http_games_router(
    router: APIRouter,
    games_service: AbstractGamesService,
    games_mapper: AbstractGamesRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP games router.

    Parameters:
    - router: APIRouter object.
    - games_service: AbstractGamesService object.
    - games_mapper: AbstractGamesRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_games_router = HttpGamesRouter(
        router=router,
        games_service=games_service,
        games_mapper=games_mapper,
        auth_service=auth_service
    )

    http_games_router.register()

def setup_fastapi_http_files_router(
    router: APIRouter,
    files_service: AbstractFilesService,
    files_mapper: AbstractFilesRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP files router.

    Parameters:
    - router: APIRouter object.
    - files_service: AbstractFilesService object.
    - files_mapper: AbstractFilesRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_files_router = HttpFilesRouter(
        router=router,
        files_service=files_service,
        files_mapper=files_mapper,
        auth_service=auth_service
    )

    http_files_router.register()

def setup_fastapi_ws_events_router(
    router: APIRouter,
    events_manager: AbstractEventsManager,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the WebSocket events router.

    Parameters:
    - router: APIRouter object.
    - events_manager: AbstractEventsManager object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    ws_events_router = WsEventsRouter(
        router=router,
        events_manager=events_manager,
        auth_service=auth_service
    )

    ws_events_router.register()

def setup_fastapi_ws_logs_router(
    router: APIRouter,
    events_manager: AbstractEventsManager,
    logs_service: AbstractLogsService,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the WebSocket logs router.

    Parameters:
    - router: APIRouter object.
    - events_manager: AbstractEventsManager object.
    - logs_service: AbstractLogsService object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    ws_logs_router = WsLogsEvents(
        router=router,
        events_manager=events_manager,
        logs_service=logs_service,
        auth_service=auth_service
    )

    ws_logs_router.register()

def setup_fastapi_ws_metrics_router(
    router: APIRouter,
    events_manager: AbstractEventsManager,
    metrics_service: AbstractMetricsService,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the WebSocket metrics router.

    Parameters:
    - router: APIRouter object.
    - events_manager: AbstractEventsManager object.
    - metrics_service: AbstractMetricsService object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    ws_metrics_router = WsMetricsEvents(
        router=router,
        events_manager=events_manager,
        metrics_service=metrics_service,
        auth_service=auth_service
    )

    ws_metrics_router.register()

def setup_fastapi_ws_servers_router(
    router: APIRouter,
    events_manager: AbstractEventsManager,
    servers_service: AbstractServersService,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the WebSocket logs router.

    Parameters:
    - router: APIRouter object.
    - events_manager: AbstractEventsManager object.
    - servers_service: AbstractServersService object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    ws_servers_router = WsServersEvents(
        router=router,
        events_manager=events_manager,
        servers_service=servers_service,
        auth_service=auth_service
    )

    ws_servers_router.register()

def setup_fastapi_routers(
    router: APIRouter,
    managers: ManagersContainer,
    mappers: MappersContainer,
    services: ServicesContainer
) -> APIRouter:
    """
    Setups the application routers.

    Parameters:
    - router: APIRouter object.
    - managers: ManagersContainer object.
    - mappers: MappersContainer object.
    - services: ServicesContainer object.

    Returns:
    - APIRouter: APIRouter object.
    """
    setup_fastapi_http_auth_router(
        router=router,
        auth_service=services.auth,
        auth_mapper=mappers.routers.auth
    )

    setup_fastapi_http_attributes_router(
        router=router,
        attributes_service=services.attributes,
        attributes_mapper=mappers.routers.attributes,
        auth_service=services.auth
    )

    setup_fastapi_http_roles_router(
        router=router,
        roles_service=services.roles,
        roles_mapper=mappers.routers.roles,
        auth_service=services.auth
    )

    setup_fastapi_http_settings_router(
        router=router,
        settings_service=services.settings,
        settings_mapper=mappers.routers.settings,
        auth_service=services.auth
    )

    setup_fastapi_http_users_router(
        router=router,
        users_service=services.users,
        users_mapper=mappers.routers.users,
        auth_service=services.auth
    )

    setup_fastapi_http_logs_router(
        router=router,
        logs_service=services.logs,
        logs_mapper=mappers.routers.logs,
        auth_service=services.auth
    )

    setup_fastapi_http_metrics_router(
        router=router,
        metrics_service=services.metrics,
        metrics_mapper=mappers.routers.metrics,
        auth_service=services.auth
    )

    setup_fastapi_http_servers_router(
        router=router,
        servers_service=services.servers,
        servers_mapper=mappers.routers.servers,
        auth_service=services.auth
    )

    setup_fastapi_http_games_router(
        router=router,
        games_service=services.games,
        games_mapper=mappers.routers.games,
        auth_service=services.auth
    )

    setup_fastapi_http_files_router(
        router=router,
        files_service=services.files,
        files_mapper=mappers.routers.files,
        auth_service=services.auth
    )

    setup_fastapi_ws_events_router(
        router=router,
        events_manager=managers.events,
        auth_service=services.auth
    )

    setup_fastapi_ws_logs_router(
        router=router,
        events_manager=managers.events,
        logs_service=services.logs,
        auth_service=services.auth
    )

    setup_fastapi_ws_metrics_router(
        router=router,
        events_manager=managers.events,
        metrics_service=services.metrics,
        auth_service=services.auth
    )

    setup_fastapi_ws_servers_router(
        router=router,
        events_manager=managers.events,
        servers_service=services.servers,
        auth_service=services.auth
    )

    return router
