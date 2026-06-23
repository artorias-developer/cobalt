#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict, List, Tuple, Callable

from orjson import loads

from domain.entities import ServerEntity
from domain.enums import ServerStatusEnum
from domain.exceptions import (
    NotFoundError,
    ConflictError
)
from domain.repositories import AbstractServersRepository
from application.contracts.loggers import AbstractLogger
from application.contracts.queues import AbstractQueue
from application.contracts.clients import AbstractCachesClient
from application.contracts.managers import (
    AbstractConnectionsManager,
    AbstractI18nManager
)
from application.contracts.services import AbstractServersService
from application.contracts.mappers import AbstractServersServiceMapper
from application.contracts.games import (
    AbstractGameModule,
    AbstractLoader
)
from application.clients.caches.shared import CacheConstants
from application.clients.containers.shared import ContainersConstants
from application.managers.connections.shared import RoomsConstants
from application.dtos import (
    ServerDto,
    ServersGetPageDto,
    ServersPageDto,
    ServerCreateDto,
    ServerUpdateDto,
    ServerExecuteDto,
    ServerStatusDto
)


class ServersService(AbstractServersService):
    """
    Servers service.
    """
    caches_client: AbstractCachesClient
    connections_manager: AbstractConnectionsManager
    servers_repository: AbstractServersRepository
    servers_mapper: AbstractServersServiceMapper
    i18n_manager: AbstractI18nManager
    queue: AbstractQueue
    logger: AbstractLogger
    game_modules: Dict[str, AbstractGameModule]

    _: Callable

    def __init__(
        self,
        caches_client: AbstractCachesClient,
        connections_manager: AbstractConnectionsManager,
        servers_repository: AbstractServersRepository,
        servers_mapper: AbstractServersServiceMapper,
        i18n_manager: AbstractI18nManager,
        queue: AbstractQueue,
        logger: AbstractLogger,
        game_modules: Dict[str, AbstractGameModule]
    ):
        self.caches_client = caches_client
        self.connections_manager = connections_manager
        self.servers_repository = servers_repository
        self.servers_mapper = servers_mapper
        self.i18n_manager = i18n_manager
        self.queue = queue
        self.logger = logger
        self.game_modules = game_modules

        self._ = i18n_manager.gettext

    async def _get_server_data(
        self,
        server: ServerEntity
    ) -> Tuple[AbstractGameModule, AbstractLoader]:
        """
        Gets a server game module and loader.

        Parameters:
        - server: ServerEntity object.

        Returns:
        - Tuple: AbstractGameModule and AbstractLoader objects.
        """
        game_module = self.game_modules.get(server.game.name)

        if not game_module:
            raise NotFoundError(self._('Game "{name}" not found').format(name=server.game.name))

        loader = game_module.loaders.get(server.loader.name)

        if not loader:
            raise NotFoundError(self._('Loader "{name}" not found').format(name=server.loader.name))

        return game_module, loader

    async def _get_server_module(
        self,
        server_id: int
    ) -> AbstractGameModule:
        """
        Gets a server game module.

        Parameters:
        - server_id: Server ID.

        Returns:
        - AbstractGameModule: AbstractGameModule object.
        """
        server = await self.get_one_by_id(
            server_id=server_id
        )

        if not server:
            raise NotFoundError(self._("Server {server_id} not found").format(server_id=server_id))

        game_module = self.game_modules.get(server.game.name)

        if not game_module:
            raise NotFoundError(self._('Game "{name}" not found').format(name=server.game.name))

        return game_module

    async def get_page(
        self,
        dto: ServersGetPageDto
    ) -> ServersPageDto:
        """
        Gets a paginated list of servers.

        Parameters:
        - dto: ServersGetPageDto object.

        Returns:
        - ServersPageDto: ServersPageDto object.
        """
        key = self.caches_client.format_pattern(
            pattern=CacheConstants.SERVERS_PAGE_KEY,
            page=dto.page,
            search=dto.search,
            sort_field=dto.sort_field,
            sort_direction=dto.sort_direction,
            limit=dto.limit
        )

        cached = await self.caches_client.get(
            key=key
        )

        if cached:
            data = loads(cached)
            return ServersPageDto.from_dict(data)

        mapped_entity = self.servers_mapper.get_page_dto_to_entity(
            dto=dto
        )

        received_entity = await self.servers_repository.get_page(
            entity=mapped_entity
        )

        if not received_entity.servers:
            raise NotFoundError(self._("Servers not found"))

        mapped_dto = self.servers_mapper.page_entity_to_dto(
            entity=received_entity
        )

        await self.caches_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.NORMAL_TTL_SECONDS
        )

        return mapped_dto

    async def get_one_by_id(
            self,
            server_id: int
    ) -> ServerDto:
        """
        Gets an existing server by ID.

        Parameters:
        - server_id: Server ID.

        Returns:
        - ServerDto: ServerDto object.
        """
        search_key = self.caches_client.format_pattern(
            pattern=CacheConstants.SERVERS_ITEM_KEY,
            server_id=server_id
        )

        cached = await self.caches_client.get(
            pattern=search_key
        )

        if cached:
            data = loads(cached)
            return ServerDto.from_dict(data)

        received_entity = await self.servers_repository.get_one_by_id(
            server_id=server_id
        )

        if not received_entity:
            raise NotFoundError(self._("Server {server_id} not found").format(server_id=server_id))

        key = self.caches_client.format_pattern(
            pattern=CacheConstants.SERVERS_ITEM_KEY,
            server_id=received_entity.id,
            game_id=received_entity.game.id,
            loader_id=received_entity.loader.id
        )

        mapped_dto = self.servers_mapper.entity_to_dto(
            entity=received_entity
        )

        await self.caches_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.NORMAL_TTL_SECONDS
        )

        return mapped_dto

    async def create_one(
        self,
        dto: ServerCreateDto
    ) -> ServerDto:
        """
        Creates a new server.

        Parameters:
        - dto: ServerCreateDto object.

        Returns:
        - ServerDto: ServerDto object.
        """
        mapped_entity = self.servers_mapper.create_dto_to_entity(
            dto=dto
        )

        created_entity = await self.servers_repository.create_one(
            entity=mapped_entity
        )

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )

        game_module, loader = await self._get_server_data(
            server=created_entity
        )

        try:
            download_link = await loader.get_download_link(
                version=created_entity.version
            )
        except NotImplementedError:
            download_link = None
        except Exception:
            await self.servers_repository.delete_one(
                server_id=created_entity.id
            )
            raise

        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=created_entity.id
        )

        await self.queue.enqueue(
            loader.servers_service.create,
            server_id=created_entity.id,
            container_name=container_name,
            version=created_entity.version,
            download_link=download_link
        )

        return self.servers_mapper.entity_to_dto(
            entity=created_entity
        )

    async def update_one(
        self,
        server_id: int,
        dto: ServerUpdateDto
    ) -> ServerDto:
        """
        Updates an existing server.

        Parameters:
        - server_id: Server ID.
        - dto: ServerUpdateDto object.

        Returns:
        - ServerDto: ServerDto object.
        """
        mapped_entity = self.servers_mapper.update_dto_to_entity(
            server_id=server_id,
            dto=dto
        )

        updated_entity = await self.servers_repository.update_one(
            entity=mapped_entity
        )

        if not updated_entity:
            raise NotFoundError(self._("Server {server_id} not found").format(server_id=server_id))

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )

        return self.servers_mapper.entity_to_dto(
            entity=updated_entity
        )

    async def delete_one(
        self,
        server_id: int
    ) -> None:
        """
        Deletes an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - None
        """
        received_entity = await self.servers_repository.get_one_by_id(
            server_id=server_id
        )

        if not received_entity:
            raise NotFoundError(self._("Server {server_id} not found").format(server_id=server_id))

        if received_entity.status not in (ServerStatusEnum.CREATED, ServerStatusEnum.FAILED):
            raise ConflictError(self._("Server {server_id} is still being installed").format(server_id=server_id))

        await self.servers_repository.delete_one(
            server_id=server_id
        )

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_ITEM_KEY,
                    server_id=server_id
                )
            ]
        )

        game_module, loader = await self._get_server_data(
            server=received_entity
        )

        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=received_entity.id
        )

        await self.queue.enqueue(
            loader.servers_service.delete,
            container_name=container_name
        )

    async def delete_many(
        self,
        server_ids: List[int]
    ) -> None:
        """
        Deletes multiple existing servers.

        Parameters:
        - server_ids: List of server IDs.

        Returns:
        - None.
        """
        received_entities = await self.servers_repository.get_many_by_ids(
            server_ids=server_ids
        )

        if not received_entities:
            raise NotFoundError(self._("Servers not found"))

        installing = [
            server for server in received_entities
            if server.status not in (ServerStatusEnum.CREATED, ServerStatusEnum.FAILED)
        ]

        if installing:
            raise ConflictError(self._("Some servers are still being installed"))

        await self.servers_repository.delete_many(
            server_ids=server_ids
        )

        patterns_to_delete = [
            self.caches_client.format_pattern(
                pattern=CacheConstants.SERVERS_PAGE_KEY
            )
        ]

        for entity in received_entities:
            patterns_to_delete.extend([
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    server_id=entity.id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_ITEM_KEY,
                    server_id=entity.id
                )
            ])

        await self.caches_client.delete(
            patterns=patterns_to_delete
        )

        for entity in received_entities:
            game_module = self.game_modules.get(entity.game.name)

            if not game_module:
                self.logger.warning(f'Game "{entity.game.name}" not found')
                continue

            loader = game_module.loaders.get(entity.loader.name)

            if not loader:
                self.logger.warning(f'Loader "{entity.loader.name}" not found')
                continue

            container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
                server_id=entity.id
            )

            await self.queue.enqueue(
                loader.servers_service.delete,
                container_name=container_name
            )

    async def start(
        self,
        server_id: int
    ) -> None:
        """
        Starts an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - None.
        """
        game_module = await self._get_server_module(
            server_id=server_id
        )

        container = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        await game_module.dependencies.clients.containers.container_start(
            container_name=container
        )

    async def stop(
        self,
        server_id: int
    ) -> None:
        """
        Stops an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - None.
        """
        game_module = await self._get_server_module(
            server_id=server_id
        )

        container = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        await game_module.dependencies.clients.containers.container_stop(
            container_name=container
        )

    async def restart(
        self,
        server_id: int
    ) -> None:
        """
        Restarts an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - None.
        """
        game_module = await self._get_server_module(
            server_id=server_id
        )

        container = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        await game_module.dependencies.clients.containers.container_restart(
            container_name=container
        )

    async def execute(
        self,
        server_id: int,
        dto: ServerExecuteDto
    ) -> None:
        """
        Executes a command inside the server container.

        Parameters:
        - server_id: Server ID.
        - dto: ServerExecuteDto object.

        Returns:
        - None.
        """
        game_module = await self._get_server_module(
            server_id=server_id
        )

        container = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        command = ["sh", "-c", f"echo \"{dto.command}\" > {ContainersConstants.SERVER_FIFO}"]

        await game_module.dependencies.clients.containers.container_execute(
            container_name=container,
            command=command
        )

    async def status(
        self,
        server_id: int
    ) -> ServerStatusDto:
        """
        Gets the server container status.

        Parameters:
        - server_id: Server ID.

        Returns:
        - ServerStatusDto: ServerStatusDto object.
        """
        game_module = await self._get_server_module(
            server_id=server_id
        )

        container = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        status = await game_module.dependencies.clients.containers.container_status(
            container_name=container
        )

        return self.servers_mapper.status_dataclass_to_dto(
            dataclass=status
        )

    async def subscribe_states(
        self,
        connection_id: int
    ) -> None:
        """
        Subscribes to servers states.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        await self.connections_manager.join_room(
            connection_id=connection_id,
            room_name=RoomsConstants.SERVERS_STATUSES_KEY
        )

    async def unsubscribe_states(
        self,
        connection_id: int
    ) -> None:
        """
        Unsubscribes from servers states.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        await self.connections_manager.leave_room(
            connection_id=connection_id,
            room_name=RoomsConstants.SERVERS_STATUSES_KEY
        )