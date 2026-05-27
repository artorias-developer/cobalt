#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from infrastructure.contracts.databases.mappers import (
    AbstractAttributesRepositoryMapper,
    AbstractGamesRepositoryMapper,
    AbstractLoadersRepositoryMapper,
    AbstractRolesRepositoryMapper,
    AbstractServersRepositoryMapper,
    AbstractSettingsRepositoryMapper,
    AbstractUsersRepositoryMapper
)
from infrastructure.databases.postgres.mappers import (
    AttributesRepositoryMapper,
    GamesRepositoryMapper,
    LoadersRepositoryMapper,
    RolesRepositoryMapper,
    ServersRepositoryMapper,
    SettingsRepositoryMapper,
    UsersRepositoryMapper
)
from composition.dataclasses import RepositoriesMappersContainer


def create_postgres_attributes_repository_mapper() -> AbstractAttributesRepositoryMapper:
    """
    Creates the attributes repository mapper.

    Parameters:
    - None.

    Returns:
    - AbstractAttributesRepositoryMapper: AbstractAttributesRepositoryMapper object.
    """
    return AttributesRepositoryMapper()

def create_postgres_games_repository_mapper(
    loaders_mapper: AbstractLoadersRepositoryMapper
) -> AbstractGamesRepositoryMapper:
    """
    Creates the games repository mapper.

    Parameters:
    - loaders_mapper: AbstractLoadersRepositoryMapper object.

    Returns:
    - AbstractGamesRepositoryMapper: AbstractGamesRepositoryMapper object.
    """
    return GamesRepositoryMapper(
        loaders_mapper=loaders_mapper
    )

def create_postgres_loaders_repository_mapper() -> AbstractLoadersRepositoryMapper:
    """
    Creates the loaders repository mapper.

    Parameters:
    - None.

    Returns:
    - AbstractLoadersRepositoryMapper: AbstractLoadersRepositoryMapper object.
    """
    return LoadersRepositoryMapper()

def create_postgres_roles_repository_mapper() -> AbstractRolesRepositoryMapper:
    """
    Creates the roles repository mapper.

    Parameters:
    - None.

    Returns:
    - AbstractRolesRepositoryMapper: AbstractRolesRepositoryMapper object.
    """
    return RolesRepositoryMapper()

def create_postgres_servers_repository_mapper(
    attributes_mapper: AbstractAttributesRepositoryMapper,
    games_mapper: AbstractGamesRepositoryMapper,
    loaders_mapper: AbstractLoadersRepositoryMapper
) -> AbstractServersRepositoryMapper:
    """
    Creates the servers repository mapper.

    Parameters:
    - attributes_mapper: AbstractAttributesRepositoryMapper object.
    - games_mapper: AbstractGamesRepositoryMapper object.
    - loaders_mapper: AbstractLoadersRepositoryMapper object.

    Returns:
    - AbstractServersRepositoryMapper: AbstractServersRepositoryMapper object.
    """
    return ServersRepositoryMapper(
        attributes_mapper=attributes_mapper,
        games_mapper=games_mapper,
        loaders_mapper=loaders_mapper
    )

def create_postgres_settings_repository_mapper() -> AbstractSettingsRepositoryMapper:
    """
    Creates the settings repository mapper.

    Parameters:
    - None.

    Returns:
    - AbstractSettingsRepositoryMapper: AbstractSettingsRepositoryMapper object.
    """
    return SettingsRepositoryMapper()

def create_postgres_users_repository_mapper(
    roles_mapper: AbstractRolesRepositoryMapper,
    settings_mapper: AbstractSettingsRepositoryMapper
) -> AbstractUsersRepositoryMapper:
    """
    Creates the users repository mapper.

    Parameters:
    - roles_mapper: AbstractRolesRepositoryMapper object.
    - settings_mapper: AbstractSettingsRepositoryMapper object.

    Returns:
    - AbstractUsersRepositoryMapper: AbstractUsersRepositoryMapper object.
    """
    return UsersRepositoryMapper(
        roles_mapper=roles_mapper,
        settings_mapper=settings_mapper
    )

def create_postgres_repositories_mappers() -> RepositoriesMappersContainer:
    """
    Creates the repositories mappers.

    Parameters:
    - None.

    Returns:
    - RepositoriesMappersContainer: RepositoriesMappersContainer object.
    """
    loaders_repository_mapper = create_postgres_loaders_repository_mapper()

    games_repository_mapper = create_postgres_games_repository_mapper(
        loaders_mapper=loaders_repository_mapper
    )

    attributes_repository_mapper = create_postgres_attributes_repository_mapper()

    servers_repository_mapper = create_postgres_servers_repository_mapper(
        attributes_mapper=attributes_repository_mapper,
        games_mapper=games_repository_mapper,
        loaders_mapper=loaders_repository_mapper
    )

    roles_repository_mapper = create_postgres_roles_repository_mapper()

    settings_repository_mapper = create_postgres_settings_repository_mapper()

    users_repository_mapper = create_postgres_users_repository_mapper(
        roles_mapper=roles_repository_mapper,
        settings_mapper=settings_repository_mapper
    )

    return RepositoriesMappersContainer(
        attributes=attributes_repository_mapper,
        games=games_repository_mapper,
        loaders=loaders_repository_mapper,
        roles=roles_repository_mapper,
        servers=servers_repository_mapper,
        settings=settings_repository_mapper,
        users=users_repository_mapper
    )
