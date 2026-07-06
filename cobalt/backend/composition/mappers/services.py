#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.mappers import (
    AbstractAttributesServiceMapper,
    AbstractGamesServiceMapper,
    AbstractLoadersServiceMapper,
    AbstractRolesServiceMapper,
    AbstractSettingsServiceMapper,
    AbstractLogsServiceMapper,
    AbstractMetricsServiceMapper,
    AbstractServersServiceMapper,
    AbstractUsersServiceMapper
)
from application.mappers import (
    AttributesServiceMapper,
    GamesServiceMapper,
    LoadersServiceMapper,
    LogsServiceMapper,
    MetricsServiceMapper,
    RolesServiceMapper,
    ServersServiceMapper,
    SettingsServiceMapper,
    UsersServiceMapper
)
from composition.dataclasses import ServicesMappersContainer


def create_attributes_service_mapper() -> AbstractAttributesServiceMapper:
    """
    Creates the attributes service mapper.

    Parameters:
    - None.

    Returns:
    - AbstractAttributesServiceMapper: AbstractAttributesServiceMapper object.
    """
    return AttributesServiceMapper()

def create_games_service_mapper(
    loaders_mapper: AbstractLoadersServiceMapper
) -> AbstractGamesServiceMapper:
    """
    Creates the games service mapper.

    Parameters:
    - loaders_mapper: AbstractLoadersServiceMapper object.

    Returns:
    - AbstractGamesServiceMapper: AbstractGamesServiceMapper object.
    """
    return GamesServiceMapper(
        loaders_mapper=loaders_mapper
    )

def create_loaders_service_mapper() -> AbstractLoadersServiceMapper:
    """
    Creates the loaders service mapper.

    Parameters:
    - None.

    Returns:
    - AbstractLoadersServiceMapper: AbstractLoadersServiceMapper object.
    """
    return LoadersServiceMapper()

def create_logs_service_mapper() -> AbstractLogsServiceMapper:
    """
    Creates the logs service mapper.

    Parameters:
    - None.

    Returns:
    - AbstractLogsServiceMapper: AbstractLogsServiceMapper object.
    """
    return LogsServiceMapper()

def create_metrics_service_mapper() -> AbstractMetricsServiceMapper:
    """
    Creates the metrics service mapper.

    Parameters:
    - None.

    Returns:
    - AbstractMetricsServiceMapper: AbstractMetricsServiceMapper object.
    """
    return MetricsServiceMapper()

def create_roles_service_mapper() -> AbstractRolesServiceMapper:
    """
    Creates the roles service mapper.

    Parameters:
    - None.

    Returns:
    - AbstractRolesServiceMapper: AbstractRolesServiceMapper object.
    """
    return RolesServiceMapper()

def create_servers_service_mapper(
    attributes_mapper: AbstractAttributesServiceMapper,
    games_mapper: AbstractGamesServiceMapper,
    loaders_mapper: AbstractLoadersServiceMapper
) -> AbstractServersServiceMapper:
    """
    Creates the servers service mapper.

    Parameters:
    - attributes_mapper: AbstractAttributesServiceMapper object.
    - games_mapper: AbstractGamesServiceMapper object.
    - loaders_mapper: AbstractLoadersServiceMapper object.

    Returns:
    - AbstractServersServiceMapper: AbstractServersServiceMapper object.
    """
    return ServersServiceMapper(
        attributes_mapper=attributes_mapper,
        games_mapper=games_mapper,
        loaders_mapper=loaders_mapper
    )

def create_settings_service_mapper() -> AbstractSettingsServiceMapper:
    """
    Creates the settings service mapper.

    Parameters:
    - None.

    Returns:
    - AbstractSettingsServiceMapper: AbstractSettingsServiceMapper object.
    """
    return SettingsServiceMapper()

def create_users_service_mapper(
    roles_mapper: AbstractRolesServiceMapper,
    settings_mapper: AbstractSettingsServiceMapper
) -> AbstractUsersServiceMapper:
    """
    Creates the users service mapper.

    Parameters:
    - roles_mapper: AbstractRolesServiceMapper object.
    - settings_mapper: AbstractSettingsServiceMapper object.

    Returns:
    - AbstractUsersServiceMapper: AbstractUsersServiceMapper object.
    """
    return UsersServiceMapper(
        roles_mapper=roles_mapper,
        settings_mapper=settings_mapper
    )

def create_services_mappers() -> ServicesMappersContainer:
    """
    Creates the services mappers.

    Parameters:
    - None.

    Returns:
    - ServicesMappersContainer: ServicesMappersContainer object.
    """
    loaders_service_mapper = create_loaders_service_mapper()

    games_service_mapper = create_games_service_mapper(
        loaders_mapper=loaders_service_mapper
    )

    attributes_service_mapper = create_attributes_service_mapper()

    logs_service_mapper = create_logs_service_mapper()

    metrics_service_mapper = create_metrics_service_mapper()

    servers_service_mapper = create_servers_service_mapper(
        attributes_mapper=attributes_service_mapper,
        games_mapper=games_service_mapper,
        loaders_mapper=loaders_service_mapper
    )

    roles_service_mapper = create_roles_service_mapper()

    settings_service_mapper = create_settings_service_mapper()

    users_service_mapper = create_users_service_mapper(
        roles_mapper=roles_service_mapper,
        settings_mapper=settings_service_mapper
    )

    return ServicesMappersContainer(
        attributes=attributes_service_mapper,
        games=games_service_mapper,
        loaders=loaders_service_mapper,
        logs=logs_service_mapper,
        metrics=metrics_service_mapper,
        roles=roles_service_mapper,
        servers=servers_service_mapper,
        settings=settings_service_mapper,
        users=users_service_mapper
    )
