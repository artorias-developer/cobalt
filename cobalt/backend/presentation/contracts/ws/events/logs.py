#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.ws.routers import AbstractWsRouter


class AbstractWsLogsEvents(AbstractWsRouter, ABC):
    """
    Abstract WebSockets events for logs-related operations.
    """

    @abstractmethod
    async def subscribe_host(self, *args: Any, **kwargs: Any) -> None:
        """
        Subscribes to host live logs.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def subscribe_server(self, *args: Any, **kwargs: Any) -> None:
        """
        Subscribes to server live logs.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_host(self, *args: Any, **kwargs: Any) -> None:
        """
        Unsubscribes from host live logs.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_server(self, *args: Any, **kwargs: Any) -> None:
        """
        Unsubscribes from server live logs.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...
