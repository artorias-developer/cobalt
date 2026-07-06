#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter

from application.contracts.managers import (
    AbstractEventsManager,
    AbstractI18nManager
)
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
    i18n_manager: AbstractI18nManager,
    auth_service: AbstractAuthService,
    auth_mapper: AbstractAuthRouterMapper
) -> None:
    """
    Setups the HTTP auth router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - auth_service: AbstractAuthService object.
    - auth_mapper: AbstractAuthRouterMapper object.

    Returns:
    - None.
    """
    http_auth_router = HttpAuthRouter(
        router=router,
        i18n_manager=i18n_manager,
        auth_service=auth_service,
        auth_mapper=auth_mapper
    )

    http_auth_router.register()


def setup_fastapi_http_attributes_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    attributes_service: AbstractAttributesService,
    attributes_mapper: AbstractAttributesRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP attributes router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - attributes_service: AbstractAttributesService object.
    - attributes_mapper: AbstractAttributesRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_attributes_router = HttpAttributesRouter(
        router=router,
        i18n_manager=i18n_manager,
        attributes_service=attributes_service,
        attributes_mapper=attributes_mapper,
        auth_service=auth_service
    )

    http_attributes_router.register()


def setup_fastapi_http_roles_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    roles_service: AbstractRolesService,
    roles_mapper: AbstractRolesRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP roles router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - roles_service: AbstractRolesService object.
    - roles_mapper: AbstractRolesRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_roles_router = HttpRolesRouter(
        router=router,
        i18n_manager=i18n_manager,
        roles_service=roles_service,
        roles_mapper=roles_mapper,
        auth_service=auth_service
    )

    http_roles_router.register()


def setup_fastapi_http_settings_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    settings_service: AbstractSettingsService,
    settings_mapper: AbstractSettingsRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP settings router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - settings_service: AbstractSettingsService object.
    - settings_mapper: AbstractSettingsRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_settings_router = HttpSettingsRouter(
        router=router,
        i18n_manager=i18n_manager,
        settings_service=settings_service,
        settings_mapper=settings_mapper,
        auth_service=auth_service
    )

    http_settings_router.register()


def setup_fastapi_http_users_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    users_service: AbstractUsersService,
    users_mapper: AbstractUsersRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP users router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - users_service: AbstractUsersService object.
    - users_mapper: AbstractUsersRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_users_router = HttpUsersRouter(
        router=router,
        i18n_manager=i18n_manager,
        users_service=users_service,
        users_mapper=users_mapper,
        auth_service=auth_service
    )

    http_users_router.register()


def setup_fastapi_http_logs_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    logs_service: AbstractLogsService,
    logs_mapper: AbstractLogsRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP logs router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - logs_service: AbstractLogsService object.
    - logs_mapper: AbstractLogsRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_logs_router = HttpLogsRouter(
        router=router,
        i18n_manager=i18n_manager,
        logs_service=logs_service,
        logs_mapper=logs_mapper,
        auth_service=auth_service
    )

    http_logs_router.register()


def setup_fastapi_http_metrics_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    metrics_service: AbstractMetricsService,
    metrics_mapper: AbstractMetricsRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP metrics router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - metrics_service: AbstractMetricsService object.
    - metrics_mapper: AbstractMetricsRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_metrics_router = HttpMetricsRouter(
        router=router,
        i18n_manager=i18n_manager,
        metrics_service=metrics_service,
        metrics_mapper=metrics_mapper,
        auth_service=auth_service
    )

    http_metrics_router.register()


def setup_fastapi_http_servers_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    servers_service: AbstractServersService,
    servers_mapper: AbstractServersRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP servers router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - servers_service: AbstractServersService object.
    - servers_mapper: AbstractServersRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_servers_router = HttpServersRouter(
        router=router,
        i18n_manager=i18n_manager,
        servers_service=servers_service,
        servers_mapper=servers_mapper,
        auth_service=auth_service
    )

    http_servers_router.register()


def setup_fastapi_http_games_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    games_service: AbstractGamesService,
    games_mapper: AbstractGamesRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP games router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - games_service: AbstractGamesService object.
    - games_mapper: AbstractGamesRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_games_router = HttpGamesRouter(
        router=router,
        i18n_manager=i18n_manager,
        games_service=games_service,
        games_mapper=games_mapper,
        auth_service=auth_service
    )

    http_games_router.register()


def setup_fastapi_http_files_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    files_service: AbstractFilesService,
    files_mapper: AbstractFilesRouterMapper,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the HTTP files router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - files_service: AbstractFilesService object.
    - files_mapper: AbstractFilesRouterMapper object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    http_files_router = HttpFilesRouter(
        router=router,
        i18n_manager=i18n_manager,
        files_service=files_service,
        files_mapper=files_mapper,
        auth_service=auth_service
    )

    http_files_router.register()


def setup_fastapi_ws_events_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    events_manager: AbstractEventsManager,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the WebSocket events router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - events_manager: AbstractEventsManager object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    ws_events_router = WsEventsRouter(
        router=router,
        i18n_manager=i18n_manager,
        events_manager=events_manager,
        auth_service=auth_service
    )

    ws_events_router.register()


def setup_fastapi_ws_logs_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    events_manager: AbstractEventsManager,
    logs_service: AbstractLogsService,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the WebSocket logs router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - events_manager: AbstractEventsManager object.
    - logs_service: AbstractLogsService object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    ws_logs_router = WsLogsEvents(
        router=router,
        i18n_manager=i18n_manager,
        events_manager=events_manager,
        logs_service=logs_service,
        auth_service=auth_service
    )

    ws_logs_router.register()


def setup_fastapi_ws_metrics_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    events_manager: AbstractEventsManager,
    metrics_service: AbstractMetricsService,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the WebSocket metrics router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - events_manager: AbstractEventsManager object.
    - metrics_service: AbstractMetricsService object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    ws_metrics_router = WsMetricsEvents(
        router=router,
        i18n_manager=i18n_manager,
        events_manager=events_manager,
        metrics_service=metrics_service,
        auth_service=auth_service
    )

    ws_metrics_router.register()


def setup_fastapi_ws_servers_router(
    router: APIRouter,
    i18n_manager: AbstractI18nManager,
    events_manager: AbstractEventsManager,
    servers_service: AbstractServersService,
    auth_service: AbstractAuthService
) -> None:
    """
    Setups the WebSocket servers router.

    Parameters:
    - router: APIRouter object.
    - i18n_manager: AbstractI18nManager object.
    - events_manager: AbstractEventsManager object.
    - servers_service: AbstractServersService object.
    - auth_service: AbstractAuthService object.

    Returns:
    - None.
    """
    ws_servers_router = WsServersEvents(
        router=router,
        i18n_manager=i18n_manager,
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
        i18n_manager=managers.i18n,
        auth_service=services.auth,
        auth_mapper=mappers.routers.auth
    )

    setup_fastapi_http_attributes_router(
        router=router,
        i18n_manager=managers.i18n,
        attributes_service=services.attributes,
        attributes_mapper=mappers.routers.attributes,
        auth_service=services.auth
    )

    setup_fastapi_http_roles_router(
        router=router,
        i18n_manager=managers.i18n,
        roles_service=services.roles,
        roles_mapper=mappers.routers.roles,
        auth_service=services.auth
    )

    setup_fastapi_http_settings_router(
        router=router,
        i18n_manager=managers.i18n,
        settings_service=services.settings,
        settings_mapper=mappers.routers.settings,
        auth_service=services.auth
    )

    setup_fastapi_http_users_router(
        router=router,
        i18n_manager=managers.i18n,
        users_service=services.users,
        users_mapper=mappers.routers.users,
        auth_service=services.auth
    )

    setup_fastapi_http_logs_router(
        router=router,
        i18n_manager=managers.i18n,
        logs_service=services.logs,
        logs_mapper=mappers.routers.logs,
        auth_service=services.auth
    )

    setup_fastapi_http_metrics_router(
        router=router,
        i18n_manager=managers.i18n,
        metrics_service=services.metrics,
        metrics_mapper=mappers.routers.metrics,
        auth_service=services.auth
    )

    setup_fastapi_http_servers_router(
        router=router,
        i18n_manager=managers.i18n,
        servers_service=services.servers,
        servers_mapper=mappers.routers.servers,
        auth_service=services.auth
    )

    setup_fastapi_http_games_router(
        router=router,
        i18n_manager=managers.i18n,
        games_service=services.games,
        games_mapper=mappers.routers.games,
        auth_service=services.auth
    )

    setup_fastapi_http_files_router(
        router=router,
        i18n_manager=managers.i18n,
        files_service=services.files,
        files_mapper=mappers.routers.files,
        auth_service=services.auth
    )

    setup_fastapi_ws_events_router(
        router=router,
        i18n_manager=managers.i18n,
        events_manager=managers.events,
        auth_service=services.auth
    )

    setup_fastapi_ws_logs_router(
        router=router,
        i18n_manager=managers.i18n,
        events_manager=managers.events,
        logs_service=services.logs,
        auth_service=services.auth
    )

    setup_fastapi_ws_metrics_router(
        router=router,
        i18n_manager=managers.i18n,
        events_manager=managers.events,
        metrics_service=services.metrics,
        auth_service=services.auth
    )

    setup_fastapi_ws_servers_router(
        router=router,
        i18n_manager=managers.i18n,
        events_manager=managers.events,
        servers_service=services.servers,
        auth_service=services.auth
    )

    return router
