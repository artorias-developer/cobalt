#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict

from domain.enums import EnvironmentEnum
from domain.repositories import (
    AbstractRolesRepository,
    AbstractUsersRepository,
    AbstractGamesRepository,
    AbstractLoadersRepository,
    AbstractServersRepository,
    AbstractSettingsRepository,
    AbstractAttributesRepository
)
from application.contracts.databases import AbstractTransactionsManager
from application.contracts.queues import AbstractQueue
from application.services.files import FilesService
from application.contracts.clients import AbstractCacheClient
from application.contracts.managers import (
    AbstractConnectionsManager,
    AbstractArchivesManager
)
from application.contracts.clients import AbstractContainersClient
from application.contracts.clients import AbstractMetricsClient
from application.contracts.games import AbstractGameModule
from application.contracts.services import (
    AbstractRolesService,
    AbstractSettingsService,
    AbstractUsersService,
    AbstractServersService,
    AbstractAuthService,
    AbstractGamesService,
    AbstractLoadersService,
    AbstractLogsService,
    AbstractMetricsService,
    AbstractAttributesService,
    AbstractFilesService
)
from application.contracts.hashers import AbstractHasher
from application.contracts.mappers import (
    AbstractRolesServiceMapper,
    AbstractUsersServiceMapper,
    AbstractGamesServiceMapper,
    AbstractLoadersServiceMapper,
    AbstractLogsServiceMapper,
    AbstractMetricsServiceMapper,
    AbstractServersServiceMapper,
    AbstractSettingsServiceMapper,
    AbstractAttributesServiceMapper
)
from application.contracts.loggers import AbstractLogger
from application.services import (
    AttributesService,
    AuthService,
    GamesService,
    LoadersService,
    LogsService,
    MetricsService,
    RolesService,
    ServersService,
    SettingsService,
    UsersService
)
from infrastructure.configs import ApplicationConfig
from composition.dataclasses import (
    ServicesContainer,
    ManagersContainer,
    ClientsContainer,
    MappersContainer,
    DatabaseContainer
)


def create_roles_service(
    cache_client: AbstractCacheClient,
    roles_repository: AbstractRolesRepository,
    roles_mapper: AbstractRolesServiceMapper,
    connections_manager: AbstractConnectionsManager
) -> AbstractRolesService:
    """
    Creates the roles service.

    Parameters:
    - cache_client: AbstractCacheClient object.
    - roles_repository: AbstractRolesRepository object.
    - roles_mapper: AbstractRolesServiceMapper object.
    - connections_manager: AbstractConnectionsManager object.

    Returns:
    - AbstractRolesService: AbstractRolesService object.
    """
    return RolesService(
        cache_client=cache_client,
        roles_repository=roles_repository,
        roles_mapper=roles_mapper,
        connections_manager=connections_manager
    )

def create_settings_service(
    config: ApplicationConfig,
    cache_client: AbstractCacheClient,
    settings_repository: AbstractSettingsRepository,
    settings_mapper: AbstractSettingsServiceMapper,
    containers_client: AbstractContainersClient,
    connections_manager: AbstractConnectionsManager,
    servers_service: AbstractServersService,
    queue: AbstractQueue,
    logger: AbstractLogger
) -> AbstractSettingsService:
    """
    Creates the settings service.

    Parameters:
    - config: ApplicationConfig object.
    - cache_client: AbstractCacheClient object.
    - settings_repository: AbstractSettingsRepository object.
    - settings_mapper: AbstractSettingsServiceMapper object.
    - containers_client: AbstractContainersClient object.
    - servers_service: AbstractServersService object.
    - connections_manager: AbstractConnectionsManager object.
    - queue: AbstractQueue object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractSettingsService: AbstractSettingsService object.
    """
    return SettingsService(
        cache_client=cache_client,
        settings_repository=settings_repository,
        settings_mapper=settings_mapper,
        containers_client=containers_client,
        servers_service=servers_service,
        connections_manager=connections_manager,
        queue=queue,
        logger=logger,
        app_containers_dir=config.server.app_containers_dir
    )

def create_users_service(
    cache_client: AbstractCacheClient,
    users_repository: AbstractUsersRepository,
    users_mapper: AbstractUsersServiceMapper,
    hasher: AbstractHasher,
    roles_service: AbstractRolesService,
    settings_service: AbstractSettingsService
) -> AbstractUsersService:
    """
    Creates the users service.

    Parameters:
    - cache_client: AbstractCacheClient.
    - users_repository: AbstractUsersRepository object.
    - users_mapper: AbstractUsersServiceMapper object.
    - hasher: AbstractHasher object.
    - roles_service: AbstractRolesService object.
    - settings_service: AbstractSettingsService object.

    Returns:
    - AbstractUsersService: AbstractUsersService object.
    """
    return UsersService(
        cache_client=cache_client,
        users_repository=users_repository,
        users_mapper=users_mapper,
        hasher=hasher,
        roles_service=roles_service,
        settings_service=settings_service
    )

def create_auth_service(
    cache_client: AbstractCacheClient,
    users_service: AbstractUsersService,
    hasher: AbstractHasher
) -> AbstractAuthService:
    """
    Creates the auth service.

    Parameters:
    - cache_client: AbstractCacheClient object.
    - users_service: AbstractUsersService object.
    - hasher: AbstractHasher object.

    Returns:
    - AbstractAuthService: AbstractAuthService object.
    """
    return AuthService(
        cache_client=cache_client,
        users_service=users_service,
        hasher=hasher
    )

def create_games_service(
    cache_client: AbstractCacheClient,
    games_repository: AbstractGamesRepository,
    games_mapper: AbstractGamesServiceMapper
) -> AbstractGamesService:
    """
    Creates the games service.

    Parameters:
    - cache_client: AbstractCacheClient object.
    - games_repository: AbstractGamesRepository object.
    - games_mapper: AbstractGamesServiceMapper object.

    Returns:
    - AbstractGamesService: AbstractGamesService object.
    """
    return GamesService(
        cache_client=cache_client,
        games_repository=games_repository,
        games_mapper=games_mapper
    )

def create_loaders_service(
    cache_client: AbstractCacheClient,
    loaders_repository: AbstractLoadersRepository,
    loaders_mapper: AbstractLoadersServiceMapper
) -> AbstractLoadersService:
    """
    Creates the loaders service.

    Parameters:
    - cache_client: AbstractCacheClient object.
    - loaders_repository: AbstractLoadersRepository object.
    - loaders_mapper: AbstractLoadersServiceMapper object.

    Returns:
    - AbstractLoadersService: AbstractLoadersService object.
    """
    return LoadersService(
        cache_client=cache_client,
        loaders_repository=loaders_repository,
        loaders_mapper=loaders_mapper
    )

def create_logs_service(
    logs_mapper: AbstractLogsServiceMapper,
    containers_client: AbstractContainersClient,
    connections_manager: AbstractConnectionsManager,
    servers_service: AbstractServersService,
    game_modules: Dict[str, AbstractGameModule],
    environment: EnvironmentEnum
) -> AbstractLogsService:
    """
    Creates the logs service.

    Parameters:
    - logs_mapper: AbstractLogsServiceMapper object.
    - containers_client: AbstractContainersClient object.
    - connections_manager: AbstractConnectionsManager object.
    - servers_service: AbstractServersService object.
    - game_modules: Game modules dictionary.
    - environment: EnvironmentEnum value.

    Returns:
    - AbstractLogsService: AbstractLogsService object.
    """
    return LogsService(
        logs_mapper=logs_mapper,
        containers_client=containers_client,
        connections_manager=connections_manager,
        servers_service=servers_service,
        game_modules=game_modules,
        app_environment=environment
    )

def create_metrics_service(
    cache_client: AbstractCacheClient,
    metrics_client: AbstractMetricsClient,
    metrics_mapper: AbstractMetricsServiceMapper,
    connections_manager: AbstractConnectionsManager
) -> AbstractMetricsService:
    """
    Creates the metrics service.

    Parameters:
    - cache_client: AbstractCacheClient object.
    - metrics_client: AbstractMetricsClient object.
    - metrics_mapper: AbstractMetricsServiceMapper object.
    - connections_manager: AbstractConnectionsManager object.

    Returns:
    - AbstractMetricsService: AbstractMetricsService object.
    """
    return MetricsService(
        cache_client=cache_client,
        metrics_client=metrics_client,
        metrics_mapper=metrics_mapper,
        connections_manager=connections_manager
    )

def create_servers_service(
    cache_client: AbstractCacheClient,
    connections_manager: AbstractConnectionsManager,
    servers_repository: AbstractServersRepository,
    servers_mapper: AbstractServersServiceMapper,
    loaders_service: AbstractLoadersService,
    transactions_manager: AbstractTransactionsManager,
    queue: AbstractQueue,
    logger: AbstractLogger,
    game_modules: Dict[str, AbstractGameModule]
) -> AbstractServersService:
    """
    Creates the servers service.

    Parameters:
    - cache_client: AbstractCacheClient object.
    - connections_manager: AbstractConnectionsManager object.
    - servers_repository: AbstractServersRepository object.
    - servers_mapper: AbstractServersServiceMapper object.
    - loaders_service: AbstractLoadersService object.
    - transactions_manager: AbstractTransaction object.
    - queue: AbstractQueue object.
    - logger: AbstractLogger object.
    - game_modules: Game modules dictionary.

    Returns:
    - AbstractServersService: AbstractServersService object.
    """
    return ServersService(
        cache_client=cache_client,
        connections_manager=connections_manager,
        servers_repository=servers_repository,
        servers_mapper=servers_mapper,
        loaders_service=loaders_service,
        transactions_manager=transactions_manager,
        queue=queue,
        logger=logger,
        game_modules=game_modules
    )

def create_attributes_service(
    cache_client: AbstractCacheClient,
    attributes_repository: AbstractAttributesRepository,
    attributes_mapper: AbstractAttributesServiceMapper
) -> AbstractAttributesService:
    """
    Creates the attributes service.

    Parameters:
    - cache_client: AbstractCacheClient object.
    - attributes_repository: AbstractAttributesRepository object.
    - attributes_mapper: AbstractAttributesServiceMapper object.

    Returns:
    - AbstractAttributesService: AbstractAttributesService object.
    """
    return AttributesService(
        cache_client=cache_client,
        attributes_repository=attributes_repository,
        attributes_mapper=attributes_mapper
    )

def create_files_service(
    config: ApplicationConfig,
    archives_manager: AbstractArchivesManager
) -> AbstractFilesService:
    """
    Creates the files service.

    Parameters:
    - config: ApplicationConfig object.
    - archives_manager: AbstractArchivesManager object.

    Returns:
    - AbstractFilesService: AbstractFilesService object.
    """
    return FilesService(
        app_containers_dir=config.server.app_containers_dir,
        archives_manager=archives_manager
    )

def create_services_container(
    config: ApplicationConfig,
    managers: ManagersContainer,
    clients: ClientsContainer,
    mappers: MappersContainer,
    database: DatabaseContainer,
    logger: AbstractLogger,
    hasher: AbstractHasher,
    queue: AbstractQueue,
    game_modules: Dict[str, AbstractGameModule]
) -> ServicesContainer:
    """
    Creates the application services container.

    Parameters:
    - config: ApplicationConfig object.
    - managers: ManagersContainer object.
    - mappers: MappersContainer object.
    - database: DatabaseContainer object.
    - logger: AbstractLogger object.
    - hasher: AbstractHasher object.
    - queue: AbstractQueue object.
    - game_modules: Game modules dictionary.

    Returns:
    - ServicesContainer: ServicesContainer object.
    """
    roles_service = create_roles_service(
        cache_client=clients.caches,
        roles_repository=database.repositories.roles,
        roles_mapper=mappers.services.roles,
        connections_manager=managers.connections
    )

    loaders_service = create_loaders_service(
        cache_client=clients.caches,
        loaders_repository=database.repositories.loaders,
        loaders_mapper=mappers.services.loaders
    )

    servers_service = create_servers_service(
        cache_client=clients.caches,
        connections_manager=managers.connections,
        servers_repository=database.repositories.servers,
        servers_mapper=mappers.services.servers,
        loaders_service=loaders_service,
        transactions_manager=database.transactions_manager,
        queue=queue,
        logger=logger,
        game_modules=game_modules
    )

    settings_service = create_settings_service(
        config=config,
        cache_client=clients.caches,
        settings_repository=database.repositories.settings,
        settings_mapper=mappers.services.settings,
        containers_client=clients.containers,
        servers_service=servers_service,
        connections_manager=managers.connections,
        queue=queue,
        logger=logger
    )

    users_service = create_users_service(
        cache_client=clients.caches,
        users_repository=database.repositories.users,
        users_mapper=mappers.services.users,
        hasher=hasher,
        roles_service=roles_service,
        settings_service=settings_service
    )

    auth_service = create_auth_service(
        cache_client=clients.caches,
        users_service=users_service,
        hasher=hasher
    )

    games_service = create_games_service(
        cache_client=clients.caches,
        games_repository=database.repositories.games,
        games_mapper=mappers.services.games
    )

    logs_service = create_logs_service(
        logs_mapper=mappers.services.logs,
        containers_client=clients.containers,
        connections_manager=managers.connections,
        servers_service=servers_service,
        game_modules=game_modules,
        environment=config.server.environment
    )

    metrics_service = create_metrics_service(
        cache_client=clients.caches,
        metrics_client=clients.metrics,
        metrics_mapper=mappers.services.metrics,
        connections_manager=managers.connections
    )

    attributes_service = create_attributes_service(
        cache_client=clients.caches,
        attributes_repository=database.repositories.attributes,
        attributes_mapper=mappers.services.attributes
    )

    files_service = create_files_service(
        config=config,
        archives_manager=managers.archives
    )

    return ServicesContainer(
        attributes=attributes_service,
        auth=auth_service,
        files=files_service,
        games=games_service,
        loaders=loaders_service,
        logs=logs_service,
        metrics=metrics_service,
        roles=roles_service,
        servers=servers_service,
        settings=settings_service,
        users=users_service
    )
