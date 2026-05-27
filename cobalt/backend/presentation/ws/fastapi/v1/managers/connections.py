#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from asyncio import Lock
from copy import deepcopy
from typing import Dict, Optional, Any, List, Tuple

from fastapi import WebSocket, WebSocketDisconnect

from application.contracts.managers import AbstractConnectionsManager
from application.contracts.loggers import AbstractLogger
from application.managers.connections.shared import Room


class ConnectionsManager(AbstractConnectionsManager):
    """
    WebSockets connections manager.
    """
    _connections: Dict[int, WebSocket]
    _rooms: Dict[str, Room]
    _lock: Lock

    logger: AbstractLogger

    def __init__(
        self,
        logger: AbstractLogger
    ):
        self.logger = logger
        self._connections = {}
        self._rooms = {}
        self._lock = Lock()

    def _leave_room(
        self,
        connection_id: int,
        room_name: str
    ) -> None:
        """
        Internal method to remove connection from a room without acquiring lock.

        Parameters:
        - connection_id: Connection ID.
        - room_name: Name of the room to leave.

        Returns:
        - None.
        """
        if room_name in self._rooms and connection_id in self._rooms[room_name].connections:
            self._rooms[room_name].connections.discard(connection_id)

            if len(self._rooms[room_name].connections) == 0:
                del self._rooms[room_name]

    def _unregister(
        self,
        connection_id: int
    ) -> None:
        """
        Internal method to unregister connection without acquiring lock.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        if connection_id not in self._connections:
            return

        for room_name, room in self._rooms.copy().items():
            if connection_id in room.connections:
                self._leave_room(connection_id, room_name)

        del self._connections[connection_id]

    async def register(
        self,
        connection_id: int,
        connection: WebSocket
    ) -> None:
        """
        Registers a new WebSockets connection.

        Parameters:
        - connection_id: Unique connection identifier.
        - connection: WebSockets object.

        Returns:
        - None.
        """
        async with self._lock:
            self._connections[connection_id] = connection

    async def unregister(
        self,
        connection_id: int
    ) -> None:
        """
        Unregisters connection and removes it from all rooms.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        async with self._lock:
            self._unregister(connection_id)

    async def disconnect(
        self,
        connection_id: int
    ) -> None:
        """
        Closes and unregisters a connection.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        async with self._lock:
            connection = self._connections.get(connection_id)

        if not connection:
            return

        try:
            await connection.close()
        except Exception:
            self.logger.exception(f"Error while closing connection {connection_id}:")
        finally:
            async with self._lock:
                self._unregister(connection_id)

    async def get_connections(self) -> Dict[int, WebSocket]:
        """
        Gets all connections.

        Parameters:
        - None.

        Returns:
        - Dict: Dictionary of connections.
        """
        async with self._lock:
            return self._connections.copy()

    async def get_room(
        self,
        room_name: str
    ) -> Optional[Room]:
        """
        Gets room by name.

        Parameters:
        - room_name: Name of the room.

        Returns:
        - Room: Room object.
        """
        async with self._lock:
            room = self._rooms.get(room_name)

        return deepcopy(room) if room else None

    async def find_rooms_by_metadata(
        self,
        **filters: Any
    ) -> List[Tuple[str, Room]]:
        """
        Finds rooms by matching metadata filters.

        Parameters:
        - **filters: Key-value pairs to match against room metadata.

        Returns:
        - List: List of tuples with room name and Room object.
        """
        async with self._lock:
            matched = []

            for room_name, room in self._rooms.items():
                if all(room.metadata.get(key) == value for key, value in filters.items()):
                    matched.append((room_name, deepcopy(room)))

        return matched

    async def join_room(
        self,
        connection_id: int,
        room_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Adds connection to a room.

        Parameters:
        - connection_id: Connection ID.
        - room_name: Name of the room to join.
        - metadata: Metadata for the room.

        Returns:
        - None.
        """
        async with self._lock:
            if connection_id not in self._connections:
                return

            if room_name not in self._rooms:
                self._rooms[room_name] = Room(
                    connections=set(),
                    metadata=metadata or {}
                )

            self._rooms[room_name].connections.add(connection_id)

    async def leave_room(
        self,
        connection_id: int,
        room_name: str
    ) -> None:
        """
        Removes connection from a room.

        Parameters:
        - connection_id: Connection ID.
        - room_name: Name of the room to leave.

        Returns:
        - None.
        """
        async with self._lock:
            self._leave_room(connection_id, room_name)

    async def send_to_room(
        self,
        room_name: str,
        data: Dict
    ) -> None:
        """
        Sends data to all connections in a room.

        Parameters:
        - room_name: Name of the room.
        - data: Data to send.

        Returns:
        - None.
        """
        async with self._lock:
            room = self._rooms.get(room_name)
            connections = (
                {
                    connection_id: self._connections[connection_id]
                    for connection_id in room.connections
                    if connection_id in self._connections
                }
                if room else {}
            )

        disconnected = set()

        for connection_id, connection in connections.items():
            try:
                await connection.send_json(data)
            except WebSocketDisconnect:
                disconnected.add(connection_id)
            except Exception:
                self.logger.exception(f'Error while sending message to room "{room_name}":')

        if disconnected:
            async with self._lock:
                for connection_id in disconnected:
                    self._unregister(connection_id)

    async def send_to_connection(
        self,
        connection_id: int,
        data: Dict
    ) -> None:
        """
        Sends data to specific connection.

        Parameters:
        - connection_id: Connection ID.
        - data: Data to send.

        Returns:
        - None.
        """
        async with self._lock:
            connection = self._connections.get(connection_id)

        if not connection:
            return

        try:
            await connection.send_json(data)
        except WebSocketDisconnect:
            async with self._lock:
                self._unregister(connection_id)
        except Exception:
            self.logger.exception(f"Error while sending message to connection {connection_id}:")