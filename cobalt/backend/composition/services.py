#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict

from application.contracts.queues import AbstractQueue
from application.services.files import FilesService
from composition import DatabaseContainer
from domain.repositories import (
    AbstractRolesRepository,
    AbstractUsersRepository,
    AbstractGamesRepository,
    AbstractLoadersRepository,
    AbstractServersRepository,
    AbstractSettingsRepository,
    AbstractAttributesRepository
)
from application.contracts.clients import AbstractCachesClient
from application.contracts.managers import (
    AbstractConnectionsManager,
    AbstractArchivesManager,
    AbstractI18nManager
)
from application.contracts.clients import AbstractContainersClient
from application.contracts.clients import AbstractMetricsClient
from application.contracts.games import AbstractGameModule
from application.contracts.services import (
    AbstractPasswordsService,
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
    PasswordsService,
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
    MappersContainer
)


def create_passwords_service(
    config: ApplicationConfig,
    logger: AbstractLogger
) -> AbstractPasswordsService:
    """
    Creates the passwords service.

    Parameters:
    - config: ApplicationConfig object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractPasswordsService: AbstractPasswordsService object.
    """
    return PasswordsService(
        logger=logger,
        global_salt=config.security.global_salt,
        bcrypt_rounds=config.security.bcrypt_rounds
    )

def create_roles_service(
    i18n_manager: AbstractI18nManager,
    caches_client: AbstractCachesClient,
    roles_repository: AbstractRolesRepository,
    roles_mapper: AbstractRolesServiceMapper,
    connections_manager: AbstractConnectionsManager
) -> AbstractRolesService:
    """
    Creates the roles service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - caches_client: AbstractCachesClient object.
    - roles_repository: AbstractRolesRepository object.
    - roles_mapper: AbstractRolesServiceMapper object.
    - connections_manager: AbstractConnectionsManager object.

    Returns:
    - AbstractRolesService: AbstractRolesService object.
    """
    return RolesService(
        i18n_manager=i18n_manager,
        caches_client=caches_client,
        roles_repository=roles_repository,
        roles_mapper=roles_mapper,
        connections_manager=connections_manager
    )

def create_settings_service(
    i18n_manager: AbstractI18nManager,
    config: ApplicationConfig,
    caches_client: AbstractCachesClient,
    settings_repository: AbstractSettingsRepository,
    settings_mapper: AbstractSettingsServiceMapper,
    containers_client: AbstractContainersClient,
    servers_service: AbstractServersService,
    queue: AbstractQueue,
    logger: AbstractLogger
) -> AbstractSettingsService:
    """
    Creates the settings service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - config: ApplicationConfig object.
    - caches_client: AbstractCachesClient object.
    - settings_repository: AbstractSettingsRepository object.
    - settings_mapper: AbstractSettingsServiceMapper object.
    - containers_client: AbstractContainersClient object.
    - servers_service: AbstractServersService object.
    - queue: AbstractQueue object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractSettingsService: AbstractSettingsService object.
    """
    return SettingsService(
        i18n_manager=i18n_manager,
        caches_client=caches_client,
        settings_repository=settings_repository,
        settings_mapper=settings_mapper,
        containers_client=containers_client,
        servers_service=servers_service,
        queue=queue,
        logger=logger,
        app_containers_dir=config.server.app_containers_dir
    )

def create_users_service(
    i18n_manager: AbstractI18nManager,
    caches_client: AbstractCachesClient,
    users_repository: AbstractUsersRepository,
    users_mapper: AbstractUsersServiceMapper,
    passwords_service: AbstractPasswordsService,
    roles_service: AbstractRolesService,
    settings_service: AbstractSettingsService
) -> AbstractUsersService:
    """
    Creates the users service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - caches_client: AbstractCachesClient.
    - users_repository: AbstractUsersRepository object.
    - users_mapper: AbstractUsersServiceMapper object.
    - passwords_service: AbstractPasswordsService object.
    - roles_service: AbstractRolesService object.
    - settings_service: AbstractSettingsService object.

    Returns:
    - AbstractUsersService: AbstractUsersService object.
    """
    return UsersService(
        i18n_manager=i18n_manager,
        caches_client=caches_client,
        users_repository=users_repository,
        users_mapper=users_mapper,
        passwords_service=passwords_service,
        roles_service=roles_service,
        settings_service=settings_service
    )

def create_auth_service(
    i18n_manager: AbstractI18nManager,
    caches_client: AbstractCachesClient,
    users_service: AbstractUsersService,
    passwords_service: AbstractPasswordsService
) -> AbstractAuthService:
    """
    Creates the auth service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - caches_client: AbstractCachesClient object.
    - users_service: AbstractUsersService object.
    - passwords_service: AbstractPasswordsService object.

    Returns:
    - AbstractAuthService: AbstractAuthService object.
    """
    return AuthService(
        i18n_manager=i18n_manager,
        caches_client=caches_client,
        users_service=users_service,
        passwords_service=passwords_service
    )

def create_games_service(
    i18n_manager: AbstractI18nManager,
    caches_client: AbstractCachesClient,
    games_repository: AbstractGamesRepository,
    games_mapper: AbstractGamesServiceMapper
) -> AbstractGamesService:
    """
    Creates the games service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - caches_client: AbstractCachesClient object.
    - games_repository: AbstractGamesRepository object.
    - games_mapper: AbstractGamesServiceMapper object.

    Returns:
    - AbstractGamesService: AbstractGamesService object.
    """
    return GamesService(
        i18n_manager=i18n_manager,
        caches_client=caches_client,
        games_repository=games_repository,
        games_mapper=games_mapper
    )

def create_loaders_service(
    i18n_manager: AbstractI18nManager,
    caches_client: AbstractCachesClient,
    loaders_repository: AbstractLoadersRepository,
    loaders_mapper: AbstractLoadersServiceMapper
) -> AbstractLoadersService:
    """
    Creates the loaders service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - caches_client: AbstractCachesClient object.
    - loaders_repository: AbstractLoadersRepository object.
    - loaders_mapper: AbstractLoadersServiceMapper object.

    Returns:
    - AbstractLoadersService: AbstractLoadersService object.
    """
    return LoadersService(
        i18n_manager=i18n_manager,
        caches_client=caches_client,
        loaders_repository=loaders_repository,
        loaders_mapper=loaders_mapper
    )

def create_logs_service(
    i18n_manager: AbstractI18nManager,
    logs_mapper: AbstractLogsServiceMapper,
    containers_client: AbstractContainersClient,
    connections_manager: AbstractConnectionsManager,
    servers_service: AbstractServersService,
    game_modules: Dict[str, AbstractGameModule]
) -> AbstractLogsService:
    """
    Creates the logs service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - logs_mapper: AbstractLogsServiceMapper object.
    - containers_client: AbstractContainersClient object.
    - connections_manager: AbstractConnectionsManager object.
    - servers_service: AbstractServersService object.
    - game_modules: Game modules dictionary.

    Returns:
    - AbstractLogsService: AbstractLogsService object.
    """
    return LogsService(
        i18n_manager=i18n_manager,
        logs_mapper=logs_mapper,
        containers_client=containers_client,
        connections_manager=connections_manager,
        servers_service=servers_service,
        game_modules=game_modules
    )

def create_metrics_service(
    i18n_manager: AbstractI18nManager,
    caches_client: AbstractCachesClient,
    metrics_client: AbstractMetricsClient,
    metrics_mapper: AbstractMetricsServiceMapper,
    connections_manager: AbstractConnectionsManager
) -> AbstractMetricsService:
    """
    Creates the metrics service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - caches_client: AbstractCachesClient object.
    - metrics_client: AbstractMetricsClient object.
    - metrics_mapper: AbstractMetricsServiceMapper object.
    - connections_manager: AbstractConnectionsManager object.

    Returns:
    - AbstractMetricsService: AbstractMetricsService object.
    """
    return MetricsService(
        i18n_manager=i18n_manager,
        caches_client=caches_client,
        metrics_client=metrics_client,
        metrics_mapper=metrics_mapper,
        connections_manager=connections_manager
    )

def create_servers_service(
    i18n_manager: AbstractI18nManager,
    caches_client: AbstractCachesClient,
    connections_manager: AbstractConnectionsManager,
    servers_repository: AbstractServersRepository,
    servers_mapper: AbstractServersServiceMapper,
    queue: AbstractQueue,
    logger: AbstractLogger,
    game_modules: Dict[str, AbstractGameModule]
) -> AbstractServersService:
    """
    Creates the servers service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - caches_client: AbstractCachesClient object.
    - connections_manager: AbstractConnectionsManager object.
    - servers_repository: AbstractServersRepository object.
    - servers_mapper: AbstractServersServiceMapper object.
    - queue: AbstractQueue object.
    - logger: AbstractLogger object.
    - game_modules: Game modules dictionary.

    Returns:
    - AbstractServersService: AbstractServersService object.
    """
    return ServersService(
        i18n_manager=i18n_manager,
        caches_client=caches_client,
        connections_manager=connections_manager,
        servers_repository=servers_repository,
        servers_mapper=servers_mapper,
        queue=queue,
        logger=logger,
        game_modules=game_modules
    )

def create_attributes_service(
    i18n_manager: AbstractI18nManager,
    caches_client: AbstractCachesClient,
    attributes_repository: AbstractAttributesRepository,
    attributes_mapper: AbstractAttributesServiceMapper
) -> AbstractAttributesService:
    """
    Creates the attributes service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - caches_client: AbstractCachesClient object.
    - attributes_repository: AbstractAttributesRepository object.
    - attributes_mapper: AbstractAttributesServiceMapper object.

    Returns:
    - AbstractAttributesService: AbstractAttributesService object.
    """
    return AttributesService(
        i18n_manager=i18n_manager,
        caches_client=caches_client,
        attributes_repository=attributes_repository,
        attributes_mapper=attributes_mapper
    )

def create_files_service(
    i18n_manager: AbstractI18nManager,
    config: ApplicationConfig,
    archives_manager: AbstractArchivesManager
) -> AbstractFilesService:
    """
    Creates the files service.

    Parameters:
    - i18n_manager: AbstractI18nManager object.
    - config: ApplicationConfig object.
    - archives_manager: AbstractArchivesManager object.

    Returns:
    - AbstractFilesService: AbstractFilesService object.
    """
    return FilesService(
        i18n_manager=i18n_manager,
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
    - queue: AbstractQueue object.
    - game_modules: Game modules dictionary.

    Returns:
    - ServicesContainer: ServicesContainer object.
    """
    passwords_service = create_passwords_service(
        config=config,
        logger=logger
    )

    roles_service = create_roles_service(
        i18n_manager=managers.i18n,
        caches_client=clients.caches,
        roles_repository=database.repositories.roles,
        roles_mapper=mappers.services.roles,
        connections_manager=managers.connections
    )

    servers_service = create_servers_service(
        i18n_manager=managers.i18n,
        caches_client=clients.caches,
        connections_manager=managers.connections,
        servers_repository=database.repositories.servers,
        servers_mapper=mappers.services.servers,
        queue=queue,
        logger=logger,
        game_modules=game_modules
    )

    settings_service = create_settings_service(
        i18n_manager=managers.i18n,
        config=config,
        caches_client=clients.caches,
        settings_repository=database.repositories.settings,
        settings_mapper=mappers.services.settings,
        containers_client=clients.containers,
        servers_service=servers_service,
        queue=queue,
        logger=logger
    )

    users_service = create_users_service(
        i18n_manager=managers.i18n,
        caches_client=clients.caches,
        users_repository=database.repositories.users,
        users_mapper=mappers.services.users,
        passwords_service=passwords_service,
        roles_service=roles_service,
        settings_service=settings_service
    )

    auth_service = create_auth_service(
        i18n_manager=managers.i18n,
        caches_client=clients.caches,
        users_service=users_service,
        passwords_service=passwords_service
    )

    games_service = create_games_service(
        i18n_manager=managers.i18n,
        caches_client=clients.caches,
        games_repository=database.repositories.games,
        games_mapper=mappers.services.games
    )

    loaders_service = create_loaders_service(
        i18n_manager=managers.i18n,
        caches_client=clients.caches,
        loaders_repository=database.repositories.loaders,
        loaders_mapper=mappers.services.loaders
    )

    logs_service = create_logs_service(
        i18n_manager=managers.i18n,
        logs_mapper=mappers.services.logs,
        containers_client=clients.containers,
        connections_manager=managers.connections,
        servers_service=servers_service,
        game_modules=game_modules
    )

    metrics_service = create_metrics_service(
        i18n_manager=managers.i18n,
        caches_client=clients.caches,
        metrics_client=clients.metrics,
        metrics_mapper=mappers.services.metrics,
        connections_manager=managers.connections
    )

    attributes_service = create_attributes_service(
        i18n_manager=managers.i18n,
        caches_client=clients.caches,
        attributes_repository=database.repositories.attributes,
        attributes_mapper=mappers.services.attributes
    )

    files_service = create_files_service(
        i18n_manager=managers.i18n,
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
        passwords=passwords_service,
        roles=roles_service,
        servers=servers_service,
        settings=settings_service,
        users=users_service
    )
