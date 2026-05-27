#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from presentation.contracts.http.mappers import (
    AbstractAttributesRouterMapper,
    AbstractGamesRouterMapper,
    AbstractLoadersRouterMapper,
    AbstractRolesRouterMapper,
    AbstractSettingsRouterMapper,
    AbstractAuthRouterMapper,
    AbstractLogsRouterMapper,
    AbstractMetricsRouterMapper,
    AbstractServersRouterMapper,
    AbstractUsersRouterMapper,
    AbstractFilesRouterMapper
)
from presentation.http.fastapi.v1.mappers import (
    AttributesRouterMapper,
    AuthRouterMapper,
    GamesRouterMapper,
    LoadersRouterMapper,
    LogsRouterMapper,
    MetricsRouterMapper,
    RolesRouterMapper,
    ServersRouterMapper,
    SettingsRouterMapper,
    UsersRouterMapper,
    FilesRouterMapper
)
from composition.dataclasses import RoutersMappersContainer


def create_fastapi_attributes_router_mapper() -> AbstractAttributesRouterMapper:
    """
    Creates the attributes router mapper.

    Parameters:
    - None.

    Returns:
    - AbstractAttributesRouterMapper: AbstractAttributesRouterMapper object.
    """
    return AttributesRouterMapper()

def create_fastapi_auth_router_mapper() -> AbstractAuthRouterMapper:
    """
    Creates the auth router mapper.

    Parameters:
    - None.

    Returns:
    - AbstractAuthRouterMapper: AbstractAuthRouterMapper object.
    """
    return AuthRouterMapper()

def create_fastapi_loaders_router_mapper() -> AbstractLoadersRouterMapper:
    """
    Creates the loaders router mapper.

    Parameters:
    - None.

    Returns:
    - AbstractLoadersRouterMapper: AbstractLoadersRouterMapper object.
    """
    return LoadersRouterMapper()

def create_fastapi_games_router_mapper(
    loaders_mapper: AbstractLoadersRouterMapper
) -> AbstractGamesRouterMapper:
    """
    Creates the games router mapper.

    Parameters:
    - loaders_mapper: AbstractLoadersRouterMapper object.

    Returns:
    - AbstractGamesRouterMapper: AbstractGamesRouterMapper object.
    """
    return GamesRouterMapper(
        loaders_mapper=loaders_mapper
    )

def create_fastapi_logs_router_mapper() -> AbstractLogsRouterMapper:
    """
    Creates the logs router mapper.

    Parameters:
    - None.

    Returns:
    - AbstractLogsRouterMapper: AbstractLogsRouterMapper object.
    """
    return LogsRouterMapper()

def create_fastapi_metrics_router_mapper() -> AbstractMetricsRouterMapper:
    """
    Creates the metrics router mapper.

    Parameters:
    - None.

    Returns:
    - AbstractMetricsRouterMapper: AbstractMetricsRouterMapper object.
    """
    return MetricsRouterMapper()

def create_fastapi_roles_router_mapper() -> AbstractRolesRouterMapper:
    """
    Creates the roles router mapper.

    Parameters:
    - None.

    Returns:
    - AbstractRolesRouterMapper: AbstractRolesRouterMapper object.
    """
    return RolesRouterMapper()

def create_fastapi_servers_router_mapper(
    attributes_mapper: AbstractAttributesRouterMapper,
    games_mapper: AbstractGamesRouterMapper,
    loaders_mapper: AbstractLoadersRouterMapper
) -> AbstractServersRouterMapper:
    """
    Creates the servers router mapper.

    Parameters:
    - attributes_mapper: AbstractAttributesRouterMapper object.
    - games_mapper: AbstractGamesRouterMapper object.
    - loaders_mapper: AbstractLoadersRouterMapper object.

    Returns:
    - AbstractServersRouterMapper: AbstractServersRouterMapper object.
    """
    return ServersRouterMapper(
        attributes_mapper=attributes_mapper,
        games_mapper=games_mapper,
        loaders_mapper=loaders_mapper
    )

def create_fastapi_settings_router_mapper() -> AbstractSettingsRouterMapper:
    """
    Creates the settings router mapper.

    Parameters:
    - None.

    Returns:
    - AbstractSettingsRouterMapper: AbstractSettingsRouterMapper object.
    """
    return SettingsRouterMapper()

def create_fastapi_users_router_mapper(
    roles_mapper: AbstractRolesRouterMapper,
    settings_mapper: AbstractSettingsRouterMapper
) -> AbstractUsersRouterMapper:
    """
    Creates the users router mapper.

    Parameters:
    - roles_mapper: AbstractRolesRouterMapper object.
    - settings_mapper: AbstractSettingsRouterMapper object.

    Returns:
    - AbstractUsersRouterMapper: AbstractUsersRouterMapper object.
    """
    return UsersRouterMapper(
        roles_mapper=roles_mapper,
        settings_mapper=settings_mapper
    )

def create_fastapi_files_router_mapper() -> AbstractFilesRouterMapper:
    """
    Creates the files router mapper.

    Parameters:
    - None.

    Returns:
    - AbstractFilesRouterMapper: AbstractFilesRouterMapper object.
    """
    return FilesRouterMapper()

def create_fastapi_routers_mappers() -> RoutersMappersContainer:
    """
    Creates the routers mappers.

    Parameters:
    - None.

    Returns:
    - RoutersMappersContainer: RoutersMappersContainer object.
    """
    attributes_router_mapper = create_fastapi_attributes_router_mapper()

    auth_router_mapper = create_fastapi_auth_router_mapper()

    logs_router_mapper = create_fastapi_logs_router_mapper()

    metrics_router_mapper = create_fastapi_metrics_router_mapper()

    loaders_mapper = create_fastapi_loaders_router_mapper()

    games_router_mapper = create_fastapi_games_router_mapper(
        loaders_mapper=loaders_mapper
    )

    servers_router_mapper = create_fastapi_servers_router_mapper(
        attributes_mapper=attributes_router_mapper,
        games_mapper=games_router_mapper,
        loaders_mapper=loaders_mapper
    )

    roles_router_mapper = create_fastapi_roles_router_mapper()

    settings_router_mapper = create_fastapi_settings_router_mapper()

    users_router_mapper = create_fastapi_users_router_mapper(
        roles_mapper=roles_router_mapper,
        settings_mapper=settings_router_mapper
    )

    files_router_mapper = create_fastapi_files_router_mapper()

    return RoutersMappersContainer(
        attributes=attributes_router_mapper,
        auth=auth_router_mapper,
        files=files_router_mapper,
        games=games_router_mapper,
        loaders=loaders_mapper,
        logs=logs_router_mapper,
        metrics=metrics_router_mapper,
        roles=roles_router_mapper,
        servers=servers_router_mapper,
        settings=settings_router_mapper,
        users=users_router_mapper
    )
