#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from asyncio import Task, Event, Lock, create_task, sleep
from typing import List, Dict, Optional, Callable

from domain.exceptions import NotFoundError
from application.contracts.services import (
    AbstractLogsService,
    AbstractServersService
)
from application.contracts.games import AbstractGameModule
from application.contracts.mappers import AbstractLogsServiceMapper
from application.contracts.clients import AbstractContainersClient
from application.contracts.managers import (
    AbstractConnectionsManager,
    AbstractI18nManager
)
from application.clients.containers.shared import ContainersConstants
from application.managers.connections.shared import RoomsConstants
from application.managers.events.shared import LogsEventsEnum
from application.dtos import (
    LogDto,
    LogsSubscribeServerDto,
    LogsUnsubscribeServerDto
)


class LogsService(AbstractLogsService):
    """
    Logs service.
    """
    _HOST_CONTAINER: str = "cobalt-backend"
    _streaming_tasks: Dict[str, Task]

    logs_mapper: AbstractLogsServiceMapper
    containers_client: AbstractContainersClient
    connections_manager: AbstractConnectionsManager
    servers_service: AbstractServersService
    i18n_manager: AbstractI18nManager
    game_modules: Dict[str, AbstractGameModule]

    _: Callable

    def __init__(
        self,
        logs_mapper: AbstractLogsServiceMapper,
        containers_client: AbstractContainersClient,
        connections_manager: AbstractConnectionsManager,
        servers_service: AbstractServersService,
        i18n_manager: AbstractI18nManager,
        game_modules: Dict[str, AbstractGameModule]
    ):
        self.logs_mapper = logs_mapper
        self.containers_client = containers_client
        self.connections_manager = connections_manager
        self.servers_service = servers_service
        self.i18n_manager = i18n_manager
        self.game_modules = game_modules

        self._ = i18n_manager.gettext
        self._streaming_tasks = {}

    async def _has_active_room(
        self,
        room_name: str
    ) -> bool:
        """
        Checks if room has active connections.

        Parameters:
        - room_name: Room name.

        Returns:
        - bool: True if room has active connections, False otherwise.
        """
        room = await self.connections_manager.get_room(room_name=room_name)
        return room is not None and len(room.connections) > 0

    async def _send_batch(
        self,
        room_name: str,
        batch_data: List,
        event: str,
        server_id: Optional[int] = None
    ) -> None:
        """
        Sends batch of logs to room.

        Parameters:
        - room_name: Room name.
        - batch_data: Batch data.
        - event: Event name.
        - server_id: Server ID (optional, only for server logs).

        Returns:
        - None.
        """
        room = await self.connections_manager.get_room(
            room_name=room_name
        )

        if room:
            data = {
                "type": "message",
                "event": event,
                "data": batch_data
            }

            if server_id is not None:
                data["server_id"] = server_id

            await self.connections_manager.send_to_room(
                room_name=room_name,
                data=data
            )

    async def _periodic_flush(
        self,
        room_name: str,
        batch: list,
        batch_lock: Lock,
        stop_flusher: Event,
        event: str,
        server_id: Optional[int] = None
    ) -> None:
        """
        Periodically flushes batch to room.

        Parameters:
        - room_name: Room name.
        - batch: Batch list.
        - batch_lock: Batch lock.
        - stop_flusher: Stop event.
        - event: Event name.
        - server_id: Server ID (optional, only for server logs).

        Returns:
        - None.
        """
        while not stop_flusher.is_set():
            await sleep(0.3)

            async with batch_lock:
                if batch:
                    await self._send_batch(room_name, batch.copy(), event, server_id)
                    batch.clear()

    async def _stream_logs_to_room(
        self,
        room_name: str,
        container_name: str,
        event: str,
        server_id: Optional[int] = None,
        timestamps: bool = False
    ) -> None:
        """
        Background task for streaming logs to a room.

        Parameters:
        - room_name: Room name to stream logs to.
        - container_name: Container name to stream logs from.
        - event: Event name.
        - server_id: Server ID (optional, only for server logs).
        - timestamps: Whether to include containers timestamps in logs.

        Returns:
        - None.
        """
        batch = []
        batch_lock = Lock()
        stop_flusher = Event()

        flusher_task = create_task(
            self._periodic_flush(
                room_name=room_name,
                batch=batch,
                batch_lock=batch_lock,
                stop_flusher=stop_flusher,
                event=event,
                server_id=server_id
            )
        )

        try:
            while await self._has_active_room(room_name):
                try:
                    logs = self.containers_client.container_stream_logs(
                        container_name=container_name,
                        timestamps=timestamps
                    )

                    async for log in logs:
                        if not await self._has_active_room(room_name):
                            break

                        log_dto = self.logs_mapper.dataclass_to_dto(
                            dataclass=log
                        )

                        async with batch_lock:
                            batch.append(log_dto.model_dump(mode="json"))

                            if len(batch) >= 100:
                                await self._send_batch(room_name, batch.copy(), event, server_id)
                                batch.clear()
                finally:
                    await sleep(1)

        finally:
            stop_flusher.set()
            await flusher_task

            async with batch_lock:
                if batch:
                    await self._send_batch(room_name, batch, event, server_id)

            if room_name in self._streaming_tasks:
                del self._streaming_tasks[room_name]

    def _requires_container_timestamps(
        self,
        game_name: str
    ) -> bool:
        """
        Checks if the game requires container log timestamps.

        Parameters:
        - game_name: Game name.

        Returns:
        - bool: True if container timestamps are required, False otherwise.
        """
        return not self.game_modules[game_name].has_logs_timestamp

    async def host_all(self) -> List[LogDto]:
        """
        Gets a list of all host logs.

        Parameters:
        - None.

        Returns:
        - List: List of LogDto objects.
        """
        logs = await self.containers_client.container_logs(
            container_name=self._HOST_CONTAINER
        )

        if not logs:
            raise NotFoundError(self._("Logs for host not found"))

        return self.logs_mapper.dataclasses_to_dtos(
            dataclasses=logs
        )

    async def server_all(
        self,
        server_id: int
    ) -> List[LogDto]:
        """
        Gets a list of all server logs.

        Parameters:
        - server_id: Server ID.

        Returns:
        - List: List of LogDto objects.
        """
        server = await self.servers_service.get_one_by_id(
            server_id=server_id
        )

        if not server:
            raise NotFoundError(self._("Server with ID {server_id} not found").format(server_id=server_id))

        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        with_timestamps = self._requires_container_timestamps(
            game_name=server.game.name
        )

        logs = await self.containers_client.container_logs(
            container_name=container_name,
            timestamps=with_timestamps
        )

        if not logs:
            raise NotFoundError(self._("Logs for server with ID {server_id} not found").format(server_id=server_id))

        return self.logs_mapper.dataclasses_to_dtos(
            dataclasses=logs
        )

    async def subscribe_host(
        self,
        connection_id: int
    ) -> None:
        """
        Subscribes to host live logs.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        room_name = RoomsConstants.HOST_LOGS_KEY

        await self.connections_manager.join_room(
            connection_id=connection_id,
            room_name=room_name,
            metadata={
                "type": "logs",
                "target": "host",
                "container_name": self._HOST_CONTAINER
            }
        )

        if room_name not in self._streaming_tasks:
            task = create_task(
                self._stream_logs_to_room(
                    room_name=room_name,
                    container_name=self._HOST_CONTAINER,
                    event=LogsEventsEnum.HOST_LOG
                )
            )

            self._streaming_tasks[room_name] = task

    async def subscribe_server(
        self,
        connection_id: int,
        dto: LogsSubscribeServerDto
    ) -> None:
        """
        Subscribes to server live logs.

        Parameters:
        - connection_id: Connection ID.
        - dto: LogsServerSubscribeDto object.

        Returns:
        - None.
        """
        room_name = RoomsConstants.SERVER_LOGS_KEY.format(
            server_id=dto.server_id
        )

        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=dto.server_id
        )

        await self.connections_manager.join_room(
            connection_id=connection_id,
            room_name=room_name,
            metadata={
                "type": "logs",
                "target": "server",
                "server_id": dto.server_id,
                "container_name": container_name
            }
        )

        if room_name not in self._streaming_tasks:
            server = await self.servers_service.get_one_by_id(
                server_id=dto.server_id
            )

            with_timestamps = self._requires_container_timestamps(
                game_name=server.game.name
            )

            task = create_task(
                self._stream_logs_to_room(
                    room_name=room_name,
                    container_name=container_name,
                    event=LogsEventsEnum.SERVER_LOG,
                    server_id=dto.server_id,
                    timestamps=with_timestamps
                )
            )

            self._streaming_tasks[room_name] = task

    async def unsubscribe_host(
        self,
        connection_id: int
    ) -> None:
        """
        Unsubscribes from host live logs.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        await self.connections_manager.leave_room(
            connection_id=connection_id,
            room_name=RoomsConstants.HOST_LOGS_KEY
        )

    async def unsubscribe_server(
        self,
        connection_id: int,
        dto: LogsUnsubscribeServerDto
    ) -> None:
        """
        Unsubscribes from server live logs.

        Parameters:
        - connection_id: Connection ID.
        - dto: LogsServerUnsubscribeDto object.

        Returns:
        - None.
        """
        room_name = RoomsConstants.SERVER_LOGS_KEY.format(
            server_id=dto.server_id
        )

        await self.connections_manager.leave_room(
            connection_id=connection_id,
            room_name=room_name
        )
