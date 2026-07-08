#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import List

from application.dtos import (
    ServerDto,
    ServersGetPageDto,
    ServersPageDto,
    ServerCreateDto,
    ServerUpdateDto,
    ServerExecuteDto,
    ServerStatusDto
)


class AbstractServersService(ABC):
    """
    Abstract servers service.
    """

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    async def upgrade_one(
        self,
        server_id: int,
        dto: ServerUpdateDto
    ) -> None:
        """
        Upgrades an existing server.

        Parameters:
        - server_id: Server ID.
        - dto: ServerUpdateDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    async def delete_one(
        self,
        server_id: int
    ) -> None:
        """
        Deletes an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...
