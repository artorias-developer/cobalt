#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple

from application.managers.connections.shared import Room


class AbstractConnectionsManager(ABC):
    """
    Abstract class for connections manager.
    """
    _connections: Dict[int, Any]
    _rooms: Dict[str, Room]

    @abstractmethod
    async def register(
        self,
        connection_id: int,
        connection: Any
    ) -> None:
        """
        Registers a new connection.

        Parameters:
        - connection_id: Unique connection ID.
        - connection: Connection object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unregister(
        self,
        connection_id: int
    ) -> None:
        """
        Unregisters a connection and removes it from all rooms.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    async def get_connections(self) -> Dict[int, Any]:
        """
        Gets all connections.

        Parameters:
        - None.

        Returns:
        - Dict: Dictionary of connections.
        """
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...