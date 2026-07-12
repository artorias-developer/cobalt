#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from asyncio import gather
from pathlib import Path
from typing import List, Coroutine, Callable

from aioshutil import rmtree
from aiofiles import os

from domain.exceptions import (
    NotFoundError,
    ConflictError
)
from domain.enums import ServerStateEnum
from domain.repositories import AbstractSettingsRepository
from application.contracts.loggers import AbstractLogger
from application.contracts.queues import AbstractQueue
from application.contracts.managers import (
    AbstractI18nManager,
    AbstractConnectionsManager
)
from application.contracts.clients import AbstractCachesClient
from application.contracts.clients import AbstractContainersClient
from application.contracts.services import (
    AbstractSettingsService,
    AbstractServersService
)
from application.contracts.mappers import AbstractSettingsServiceMapper
from application.clients.caches.shared import CacheConstants
from application.clients.containers.shared import ContainersConstants
from application.dtos import (
    SettingsDto,
    SettingsUpdateDto,
    ServersGetPageDto,
    UserDto
)


class SettingsService(AbstractSettingsService):
    """
    Settings service.
    """
    caches_client: AbstractCachesClient
    settings_repository: AbstractSettingsRepository
    settings_mapper: AbstractSettingsServiceMapper
    containers_client: AbstractContainersClient
    servers_service: AbstractServersService
    connections_manager: AbstractConnectionsManager
    i18n_manager: AbstractI18nManager
    queue: AbstractQueue
    logger: AbstractLogger
    app_containers_dir: Path

    _: Callable

    def __init__(
        self,
        caches_client: AbstractCachesClient,
        settings_repository: AbstractSettingsRepository,
        settings_mapper: AbstractSettingsServiceMapper,
        containers_client: AbstractContainersClient,
        servers_service: AbstractServersService,
        connections_manager: AbstractConnectionsManager,
        i18n_manager: AbstractI18nManager,
        queue: AbstractQueue,
        logger: AbstractLogger,
        app_containers_dir: Path
    ):
        self.caches_client = caches_client
        self.settings_repository = settings_repository
        self.settings_mapper = settings_mapper
        self.containers_client = containers_client
        self.servers_service = servers_service
        self.connections_manager = connections_manager
        self.i18n_manager = i18n_manager
        self.queue = queue
        self.logger = logger
        self.app_containers_dir = app_containers_dir

        self._ = i18n_manager.gettext

    @staticmethod
    async def _gather_in_batches(
        coroutines: List[Coroutine],
        batch_size: int = 5
    ) -> List:
        """
        Runs coroutines in batches.

        Parameters:
        - coroutines: List of coroutines.
        - batch_size: Batch size.

        Returns:
        - List: List of results.
        """
        results = []

        for item in range(0, len(coroutines), batch_size):
            batch = coroutines[item:item + batch_size]
            results.extend(await gather(*batch))

        return results

    async def _cleanup_containers(
        self,
        protected_names: List[str]
    ) -> None:
        """
        Performs the cleanup of unused containers, images, volumes and directories.

        Parameters:
        - protected_names: List of container names to protect from removal.

        Returns:
        - None.
        """
        try:
            protected = set(protected_names)

            containers = await self.containers_client.container_list(
                all_containers=True,
                filters={
                    "label": [
                        f"managed_by={ContainersConstants.MANAGED_BY}",
                        "cobalt_server=true"
                    ]
                }
            )

            inspects = await self._gather_in_batches(
                coroutines=[container.show() for container in containers]
            )

            for container, inspect in zip(containers, inspects):
                name = inspect.get("Name", "").lstrip("/")

                if name in protected:
                    continue

                try:
                    await container.delete(force=True)
                except Exception:
                    self.logger.exception(f'Error while removing container "{name}":')

            await self.containers_client.image_prune(
                filters={
                    "label": [
                        f"managed_by={ContainersConstants.MANAGED_BY}"
                    ],
                    "dangling": [
                        "false"
                    ]
                }
            )

            await self.containers_client.volume_prune(
                filters={
                    "label": [
                        f"managed_by={ContainersConstants.MANAGED_BY}"
                    ],
                    "all": [
                        "true"
                    ]
                }
            )

            await self.containers_client.builder_prune(
                all_cache=True
            )

            container_dir = await os.scandir(self.app_containers_dir)

            for directory in container_dir:
                if directory.name in protected:
                    continue

                if await os.path.isdir(directory.path):
                    try:
                        await rmtree(directory.path)
                    except Exception:
                        self.logger.exception(f'Error removing folder "{directory.path}":')

        except Exception:
            self.logger.exception("Error during cleanup:")

    async def update_one(
        self,
        user_id: int,
        current_user: UserDto,
        dto: SettingsUpdateDto
    ) -> SettingsDto:
        """
        Updates existing settings.

        Parameters:
        - user_id: User ID.
        - current_user: UserDto object.
        - dto: SettingsUpdateDto object.

        Returns:
        - SettingsDto: SettingsDto object.
        """
        mapped_entity = self.settings_mapper.update_dto_to_entity(
            dto=dto
        )

        updated_entity = await self.settings_repository.update_one(
            user_id=user_id,
            entity=mapped_entity
        )

        if not updated_entity:
            raise NotFoundError(self._("Settings for user with ID {user_id} not found").format(user_id=user_id))

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SETTINGS_ITEM_KEY,
                    user_id=user_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.USERS_ITEM_KEY,
                    user_id=user_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.USERS_PAGE_KEY
                )
            ]
        )

        if current_user.settings.language.value != updated_entity.language.value:
            await self.connections_manager.disconnect(
                connection_id=current_user.id
            )

        return self.settings_mapper.entity_to_dto(
            entity=updated_entity
        )

    async def clear_cache(self) -> None:
        """
        Clears application cached data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        await self.caches_client.clear()

    async def clear_containers(self) -> None:
        """
        Clears unused containers data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        servers = []
        current_page = 1
        total_pages = 1

        while current_page <= total_pages:
            servers_page_dto = ServersGetPageDto(
                page=current_page,
                limit=100
            )

            try:
                servers_page = await self.servers_service.get_page(
                    dto=servers_page_dto
                )
            except NotFoundError:
                break

            servers.extend(servers_page.servers)

            total_pages = servers_page.pages
            current_page += 1

        installing = any(
            server.state in (ServerStateEnum.PENDING, ServerStateEnum.PROCESSING)
            for server in servers
        )

        if installing:
            raise ConflictError(self._("Cannot clear containers while servers are being created"))

        upgrading = any(
            server.state == ServerStateEnum.UPGRADING
            for server in servers
        )

        if upgrading:
            raise ConflictError(self._("Cannot clear containers while servers are being upgraded"))

        server_container_names = [
            ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
                server_id=server.id
            )
            for server in servers
        ]

        await self.queue.enqueue(
            self._cleanup_containers,
            protected_names=server_container_names
        )
