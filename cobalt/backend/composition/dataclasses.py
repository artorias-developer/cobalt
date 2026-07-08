#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass
from typing import Any

from application.contracts.databases import AbstractTransactionsManager
from domain.repositories import (
    AbstractAttributesRepository,
    AbstractGamesRepository,
    AbstractLoadersRepository,
    AbstractRolesRepository,
    AbstractServersRepository,
    AbstractSettingsRepository,
    AbstractUsersRepository
)
from application.contracts.queues import AbstractQueue
from application.contracts.clients import AbstractCachesClient
from application.contracts.mappers import (
    AbstractAttributesServiceMapper,
    AbstractGamesServiceMapper,
    AbstractLoadersServiceMapper,
    AbstractLogsServiceMapper,
    AbstractMetricsServiceMapper,
    AbstractRolesServiceMapper,
    AbstractServersServiceMapper,
    AbstractSettingsServiceMapper,
    AbstractUsersServiceMapper
)
from application.contracts.services import (
    AbstractAttributesService,
    AbstractAuthService,
    AbstractGamesService,
    AbstractLoadersService,
    AbstractLogsService,
    AbstractMetricsService,
    AbstractPasswordsService,
    AbstractRolesService,
    AbstractServersService,
    AbstractSettingsService,
    AbstractUsersService,
    AbstractFilesService
)
from application.contracts.managers import (
    AbstractEventsManager,
    AbstractConnectionsManager,
    AbstractArchivesManager,
    AbstractI18nManager
)
from application.contracts.clients import AbstractMetricsClient
from application.contracts.clients import AbstractContainersClient
from application.contracts.loggers import AbstractLogger
from infrastructure.contracts.schedulers import (
    AbstractScheduler,
    AbstractJob
)
from infrastructure.contracts.databases.mappers import (
    AbstractAttributesRepositoryMapper,
    AbstractGamesRepositoryMapper,
    AbstractLoadersRepositoryMapper,
    AbstractRolesRepositoryMapper,
    AbstractServersRepositoryMapper,
    AbstractSettingsRepositoryMapper,
    AbstractUsersRepositoryMapper
)
from presentation.contracts.http.mappers import (
    AbstractAttributesRouterMapper,
    AbstractAuthRouterMapper,
    AbstractGamesRouterMapper,
    AbstractLoadersRouterMapper,
    AbstractLogsRouterMapper,
    AbstractMetricsRouterMapper,
    AbstractRolesRouterMapper,
    AbstractServersRouterMapper,
    AbstractSettingsRouterMapper,
    AbstractUsersRouterMapper,
    AbstractFilesRouterMapper
)


@dataclass(slots=True)
class SchedulerJob:
    name: str
    instance: AbstractJob
    trigger: Any

@dataclass(slots=True)
class ManagersContainer:
    i18n: AbstractI18nManager
    events: AbstractEventsManager
    connections: AbstractConnectionsManager
    archives: AbstractArchivesManager

@dataclass(slots=True)
class ClientsContainer:
    caches: AbstractCachesClient
    metrics: AbstractMetricsClient
    containers: AbstractContainersClient

@dataclass(slots=True)
class RoutersMappersContainer:
    attributes: AbstractAttributesRouterMapper
    auth: AbstractAuthRouterMapper
    files: AbstractFilesRouterMapper
    games: AbstractGamesRouterMapper
    loaders: AbstractLoadersRouterMapper
    logs: AbstractLogsRouterMapper
    metrics: AbstractMetricsRouterMapper
    roles: AbstractRolesRouterMapper
    servers: AbstractServersRouterMapper
    settings: AbstractSettingsRouterMapper
    users: AbstractUsersRouterMapper

@dataclass(slots=True)
class ServicesMappersContainer:
    attributes: AbstractAttributesServiceMapper
    games: AbstractGamesServiceMapper
    loaders: AbstractLoadersServiceMapper
    logs: AbstractLogsServiceMapper
    metrics: AbstractMetricsServiceMapper
    roles: AbstractRolesServiceMapper
    servers: AbstractServersServiceMapper
    settings: AbstractSettingsServiceMapper
    users: AbstractUsersServiceMapper

@dataclass(slots=True)
class RepositoriesMappersContainer:
    attributes: AbstractAttributesRepositoryMapper
    games: AbstractGamesRepositoryMapper
    loaders: AbstractLoadersRepositoryMapper
    roles: AbstractRolesRepositoryMapper
    servers: AbstractServersRepositoryMapper
    settings: AbstractSettingsRepositoryMapper
    users: AbstractUsersRepositoryMapper

@dataclass(slots=True)
class MappersContainer:
    routers: RoutersMappersContainer
    services: ServicesMappersContainer
    repositories: RepositoriesMappersContainer

@dataclass(slots=True)
class ServicesContainer:
    attributes: AbstractAttributesService
    auth: AbstractAuthService
    files: AbstractFilesService
    games: AbstractGamesService
    loaders: AbstractLoadersService
    logs: AbstractLogsService
    metrics: AbstractMetricsService
    passwords: AbstractPasswordsService
    roles: AbstractRolesService
    servers: AbstractServersService
    settings: AbstractSettingsService
    users: AbstractUsersService

@dataclass(slots=True)
class RepositoriesContainer:
    attributes: AbstractAttributesRepository
    games: AbstractGamesRepository
    loaders: AbstractLoadersRepository
    roles: AbstractRolesRepository
    servers: AbstractServersRepository
    settings: AbstractSettingsRepository
    users: AbstractUsersRepository

@dataclass(slots=True)
class DatabaseContainer:
    repositories: RepositoriesContainer
    transactions_manager: AbstractTransactionsManager

@dataclass(slots=True)
class ApplicationContainer:
    logger: AbstractLogger
    scheduler: AbstractScheduler
    queue: AbstractQueue
    managers: ManagersContainer
    clients: ClientsContainer
    mappers: MappersContainer
    services: ServicesContainer
    database: DatabaseContainer
