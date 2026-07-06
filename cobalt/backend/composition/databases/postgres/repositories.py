#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.repositories import (
    AbstractAttributesRepository,
    AbstractGamesRepository,
    AbstractLoadersRepository,
    AbstractRolesRepository,
    AbstractServersRepository,
    AbstractSettingsRepository,
    AbstractUsersRepository
)
from application.contracts.loggers import AbstractLogger
from application.contracts.managers import AbstractI18nManager
from infrastructure.contracts.databases.mappers import (
    AbstractAttributesRepositoryMapper,
    AbstractGamesRepositoryMapper,
    AbstractLoadersRepositoryMapper,
    AbstractRolesRepositoryMapper,
    AbstractServersRepositoryMapper,
    AbstractSettingsRepositoryMapper,
    AbstractUsersRepositoryMapper
)
from infrastructure.databases.postgres.repositories import (
    AttributesRepository,
    GamesRepository,
    LoadersRepository,
    RolesRepository,
    ServersRepository,
    SettingsRepository,
    UsersRepository
)
from composition.dataclasses import (
    RepositoriesContainer,
    RepositoriesMappersContainer,
    ManagersContainer
)


def create_postgres_attributes_repository(
    async_session: async_sessionmaker,
    attributes_mapper: AbstractAttributesRepositoryMapper,
    i18n_manager: AbstractI18nManager,
    logger: AbstractLogger
) -> AbstractAttributesRepository:
    """
    Creates the attributes repository.

    Parameters:
    - async_session: Async session factory.
    - attributes_mapper: AbstractAttributesRepositoryMapper object.
    - i18n_manager: AbstractI18nManager object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractAttributesRepository: AbstractAttributesRepository object.
    """
    return AttributesRepository(
        async_session=async_session,
        attributes_mapper=attributes_mapper,
        i18n_manager=i18n_manager,
        logger=logger
    )

def create_postgres_games_repository(
    async_session: async_sessionmaker,
    games_mapper: AbstractGamesRepositoryMapper,
    i18n_manager: AbstractI18nManager,
    logger: AbstractLogger
) -> AbstractGamesRepository:
    """
    Creates the games repository.

    Parameters:
    - async_session: Async session factory.
    - games_mapper: AbstractGamesRepositoryMapper object.
    - i18n_manager: AbstractI18nManager object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractGamesRepository: AbstractGamesRepository object.
    """
    return GamesRepository(
        async_session=async_session,
        games_mapper=games_mapper,
        i18n_manager=i18n_manager,
        logger=logger
    )

def create_postgres_loaders_repository(
    async_session: async_sessionmaker,
    loaders_mapper: AbstractLoadersRepositoryMapper,
    i18n_manager: AbstractI18nManager,
    logger: AbstractLogger
) -> AbstractLoadersRepository:
    """
    Creates the loaders repository.

    Parameters:
    - async_session: Async session factory.
    - loaders_mapper: AbstractLoadersRepositoryMapper object.
    - i18n_manager: AbstractI18nManager object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractLoadersRepository: AbstractLoadersRepository object.
    """
    return LoadersRepository(
        async_session=async_session,
        loaders_mapper=loaders_mapper,
        i18n_manager=i18n_manager,
        logger=logger
    )

def create_postgres_roles_repository(
    async_session: async_sessionmaker,
    roles_mapper: AbstractRolesRepositoryMapper,
    i18n_manager: AbstractI18nManager,
    logger: AbstractLogger
) -> AbstractRolesRepository:
    """
    Creates the roles repository.

    Parameters:
    - async_session: Async session factory.
    - roles_mapper: AbstractRolesRepositoryMapper object.
    - i18n_manager: AbstractI18nManager object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractRolesRepository: AbstractRolesRepository object.
    """
    return RolesRepository(
        async_session=async_session,
        roles_mapper=roles_mapper,
        i18n_manager=i18n_manager,
        logger=logger
    )

def create_postgres_servers_repository(
    async_session: async_sessionmaker,
    servers_mapper: AbstractServersRepositoryMapper,
    i18n_manager: AbstractI18nManager,
    logger: AbstractLogger
) -> AbstractServersRepository:
    """
    Creates the servers repository.

    Parameters:
    - async_session: Async session factory.
    - servers_mapper: AbstractServersRepositoryMapper object.
    - i18n_manager: AbstractI18nManager object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractServersRepository: AbstractServersRepository object.
    """
    return ServersRepository(
        async_session=async_session,
        servers_mapper=servers_mapper,
        i18n_manager=i18n_manager,
        logger=logger
    )

def create_postgres_settings_repository(
    async_session: async_sessionmaker,
    settings_mapper: AbstractSettingsRepositoryMapper,
    logger: AbstractLogger
) -> AbstractSettingsRepository:
    """
    Creates the settings repository.

    Parameters:
    - async_session: Async session factory.
    - settings_mapper: AbstractSettingsRepositoryMapper object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractSettingsRepository: AbstractSettingsRepository object.
    """
    return SettingsRepository(
        async_session=async_session,
        settings_mapper=settings_mapper,
        logger=logger
    )

def create_postgres_users_repository(
    async_session: async_sessionmaker,
    users_mapper: AbstractUsersRepositoryMapper,
    i18n_manager: AbstractI18nManager,
    logger: AbstractLogger
) -> AbstractUsersRepository:
    """
    Creates the users repository.

    Parameters:
    - async_session: Async session factory.
    - users_mapper: AbstractUsersRepositoryMapper object.
    - i18n_manager: AbstractI18nManager object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractUsersRepository: AbstractUsersRepository object.
    """
    return UsersRepository(
        async_session=async_session,
        users_mapper=users_mapper,
        i18n_manager=i18n_manager,
        logger=logger
    )

def create_postgres_repositories(
    session_factory: async_sessionmaker,
    mappers: RepositoriesMappersContainer,
    managers: ManagersContainer,
    logger: AbstractLogger
) -> RepositoriesContainer:
    """
    Creates the application repositories.

    Parameters:
    - session_factory: async_sessionmaker object.
    - mappers: RepositoriesMappersContainer object.
    - managers: ManagersContainer object.
    - logger: AbstractLogger object.

    Returns:
    - RepositoriesContainer: RepositoriesContainer object.
    """
    attributes_repository = create_postgres_attributes_repository(
        async_session=session_factory,
        attributes_mapper=mappers.attributes,
        i18n_manager=managers.i18n,
        logger=logger
    )

    games_repository = create_postgres_games_repository(
        async_session=session_factory,
        games_mapper=mappers.games,
        i18n_manager=managers.i18n,
        logger=logger
    )

    loaders_repository = create_postgres_loaders_repository(
        async_session=session_factory,
        loaders_mapper=mappers.loaders,
        i18n_manager=managers.i18n,
        logger=logger
    )

    roles_repository = create_postgres_roles_repository(
        async_session=session_factory,
        roles_mapper=mappers.roles,
        i18n_manager=managers.i18n,
        logger=logger
    )

    servers_repository = create_postgres_servers_repository(
        async_session=session_factory,
        servers_mapper=mappers.servers,
        i18n_manager=managers.i18n,
        logger=logger
    )

    settings_repository = create_postgres_settings_repository(
        async_session=session_factory,
        settings_mapper=mappers.settings,
        logger=logger
    )

    users_repository = create_postgres_users_repository(
        async_session=session_factory,
        users_mapper=mappers.users,
        i18n_manager=managers.i18n,
        logger=logger
    )

    return RepositoriesContainer(
        attributes=attributes_repository,
        games=games_repository,
        loaders=loaders_repository,
        roles=roles_repository,
        servers=servers_repository,
        settings=settings_repository,
        users=users_repository
    )
