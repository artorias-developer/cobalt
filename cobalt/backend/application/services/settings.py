#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from asyncio import gather
from pathlib import Path
from typing import Awaitable, Coroutine, Dict, List, Optional, Set

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
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.clients import AbstractCacheClient
from application.contracts.clients import AbstractContainersClient
from application.contracts.services import (
    AbstractSettingsService,
    AbstractServersService,
    AbstractUsersService
)
from application.contracts.mappers import AbstractSettingsServiceMapper
from application.clients.caches.shared import CacheConstants
from application.clients.containers.shared import ContainersConstants
from application.managers.events.shared import ServerEventEnum
from application.managers.connections.shared import RoomsConstants
from application.dtos import (
    SettingsDto,
    SettingsUpdateDto,
    ServersGetPageDto,
    ServerUpdateDto
)


class SettingsService(AbstractSettingsService):
    """
    Settings service.
    """
    _STUCK_STATES_MAP = {
        ServerStateEnum.PENDING: ServerStateEnum.FAILED,
        ServerStateEnum.PROCESSING: ServerStateEnum.FAILED,
        ServerStateEnum.UPGRADING: ServerStateEnum.UPGRADE_FAILED
    }

    cache_client: AbstractCacheClient
    settings_repository: AbstractSettingsRepository
    settings_mapper: AbstractSettingsServiceMapper
    containers_client: AbstractContainersClient
    servers_service: AbstractServersService
    users_service: AbstractUsersService
    connections_manager: AbstractConnectionsManager
    queue: AbstractQueue
    logger: AbstractLogger
    app_containers_dir: Path

    def __init__(
        self,
        cache_client: AbstractCacheClient,
        settings_repository: AbstractSettingsRepository,
        settings_mapper: AbstractSettingsServiceMapper,
        containers_client: AbstractContainersClient,
        servers_service: AbstractServersService,
        users_service: AbstractUsersService,
        connections_manager: AbstractConnectionsManager,
        queue: AbstractQueue,
        logger: AbstractLogger,
        app_containers_dir: Path
    ):
        self.cache_client = cache_client
        self.settings_repository = settings_repository
        self.settings_mapper = settings_mapper
        self.containers_client = containers_client
        self.servers_service = servers_service
        self.users_service = users_service
        self.connections_manager = connections_manager
        self.queue = queue
        self.logger = logger
        self.app_containers_dir = app_containers_dir

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

    async def _get_all_servers(self) -> List:
        """
        Gets all servers by walking through all pages.

        Parameters:
        - None.

        Returns:
        - List: List of servers.
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

        return servers

    async def _run_cleanup_step(
        self,
        description: str,
        step: Awaitable
    ) -> None:
        """
        Runs a single cleanup step so that its failure does not interrupt the following ones.

        Parameters:
        - description: Step description used in the error log.
        - step: Awaitable to run.

        Returns:
        - None.
        """
        try:
            await step
        except Exception:
            self.logger.exception(f'Error during cleanup ({description}):')

    async def _inspect_container(
        self,
        container
    ) -> Optional[Dict]:
        """
        Inspects a container. Returns None if the container cannot be inspected
        (for example, it was removed in the meantime).

        Parameters:
        - container: Container object.

        Returns:
        - Optional[Dict]: Container inspect data or None.
        """
        try:
            return await container.show()
        except Exception:
            self.logger.exception("Error while inspecting container:")
            return None

    async def _remove_unused_containers(
        self,
        protected: Set[str]
    ) -> None:
        """
        Removes all managed server containers except the protected ones.

        Parameters:
        - protected: Set of container names to protect from removal.

        Returns:
        - None.
        """
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
            coroutines=[self._inspect_container(container) for container in containers]
        )

        for container, inspect in zip(containers, inspects):
            if inspect is None:
                continue

            name = inspect.get("Name", "").lstrip("/")

            if name in protected:
                continue

            try:
                await container.delete(force=True)
            except Exception:
                self.logger.exception(f'Error while removing container "{name}":')

    async def _remove_unused_directories(
        self,
        protected: Set[str]
    ) -> None:
        """
        Removes all server directories except the protected ones.

        Parameters:
        - protected: Set of directory names to protect from removal.

        Returns:
        - None.
        """
        container_dir = await os.scandir(self.app_containers_dir)

        for directory in container_dir:
            if directory.name in protected:
                continue

            if await os.path.isdir(directory.path):
                try:
                    await rmtree(directory.path)
                except Exception:
                    self.logger.exception(f'Error removing folder "{directory.path}":')

    async def _cleanup_containers(
        self,
        protected_names: List[str]
    ) -> None:
        """
        Performs the cleanup of unused containers, images, volumes and directories.
        Every step runs independently: a failure in one does not stop the others.

        Parameters:
        - protected_names: List of container names to protect from removal.

        Returns:
        - None.
        """
        protected = set(protected_names)

        await self._run_cleanup_step(
            description="containers",
            step=self._remove_unused_containers(protected)
        )

        await self._run_cleanup_step(
            description="images",
            step=self.containers_client.image_prune(
                filters={
                    "label": [
                        f"managed_by={ContainersConstants.MANAGED_BY}"
                    ],
                    "dangling": [
                        "false"
                    ]
                }
            )
        )

        await self._run_cleanup_step(
            description="volumes",
            step=self.containers_client.volume_prune(
                filters={
                    "label": [
                        f"managed_by={ContainersConstants.MANAGED_BY}"
                    ],
                    "all": [
                        "true"
                    ]
                }
            )
        )

        await self._run_cleanup_step(
            description="builder cache",
            step=self.containers_client.builder_prune(
                all_cache=True
            )
        )

        await self._run_cleanup_step(
            description="directories",
            step=self._remove_unused_directories(protected)
        )

    async def update_one(
        self,
        user_id: int,
        dto: SettingsUpdateDto
    ) -> SettingsDto:
        """
        Updates existing settings.

        Parameters:
        - user_id: User ID.
        - dto: SettingsUpdateDto object.

        Returns:
        - SettingsDto: SettingsDto object.
        """
        previous_user = await self.users_service.get_one_by_id(
            user_id=user_id
        )

        mapped_entity = self.settings_mapper.update_dto_to_entity(
            dto=dto
        )

        updated_entity = await self.settings_repository.update_one(
            user_id=user_id,
            entity=mapped_entity
        )

        if not updated_entity:
            raise NotFoundError("Settings for user with ID {user_id} not found", user_id=user_id)

        await self.cache_client.delete(
            patterns=[
                self.cache_client.format_pattern(
                    pattern=CacheConstants.SETTINGS_ITEM_KEY,
                    user_id=user_id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.USERS_ITEM_KEY,
                    user_id=user_id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.USERS_PAGE_KEY
                )
            ]
        )

        if previous_user.settings.language.value != updated_entity.language.value:
            await self.connections_manager.disconnect(
                connection_id=previous_user.id
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
        await self.cache_client.clear()

    async def clear_containers(self) -> None:
        """
        Clears unused containers data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        servers = await self._get_all_servers()

        installing = any(
            server.state in (ServerStateEnum.PENDING, ServerStateEnum.PROCESSING)
            for server in servers
        )

        if installing:
            raise ConflictError("Cannot clear containers while servers are being created")

        upgrading = any(
            server.state == ServerStateEnum.UPGRADING
            for server in servers
        )

        if upgrading:
            raise ConflictError("Cannot clear containers while servers are being upgraded")

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

    async def reset_stuck_containers(self) -> None:
        """
        Moves servers stuck in an in-progress state to the matching failed state:
        PENDING and PROCESSING become FAILED, UPGRADING becomes UPGRADE_FAILED.

        Parameters:
        - None.

        Returns:
        - None.
        """
        servers = await self._get_all_servers()

        for server in servers:
            failed_state = self._STUCK_STATES_MAP.get(server.state)

            if failed_state is None:
                continue

            try:
                await self.servers_service.update_one(
                    server_id=server.id,
                    dto=ServerUpdateDto(
                        state=failed_state,
                        version=None
                    )
                )
            except NotFoundError:
                continue

            await self.connections_manager.send_to_room(
                room_name=RoomsConstants.SERVERS_STATES_KEY,
                data={
                    "type": "message",
                    "event": ServerEventEnum.SERVER_STATE,
                    "data": {
                        "server_id": server.id,
                        "state": failed_state
                    }
                }
            )