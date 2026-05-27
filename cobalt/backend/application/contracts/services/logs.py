#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import List

from application.dtos import (
    LogDto,
    LogsSubscribeServerDto,
    LogsUnsubscribeServerDto
)


class AbstractLogsService(ABC):
    """
    Abstract logs service.
    """

    @abstractmethod
    async def host_all(self) -> List[LogDto]:
        """
        Gets a list of all host logs.

        Parameters:
        - None.

        Returns:
        - List: List of LogDto objects.
        """
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...
