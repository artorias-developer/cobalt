#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.ws.routers import AbstractWsRouter


class AbstractWsMetricsEvents(AbstractWsRouter, ABC):
    """
    Abstract WebSockets events for metrics-related operations.
    """

    @abstractmethod
    async def subscribe_host_cpu(self, *args: Any, **kwargs: Any) -> None:
        """
        Subscribes to host CPU live metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_host_cpu(self, *args: Any, **kwargs: Any) -> None:
        """
        Unsubscribes from host CPU live metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def subscribe_host_ram(self, *args: Any, **kwargs: Any) -> None:
        """
        Subscribes to host RAM live metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_host_ram(self, *args: Any, **kwargs: Any) -> None:
        """
        Unsubscribes from host RAM live metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def subscribe_server_cpu(self, *args: Any, **kwargs: Any) -> None:
        """
        Subscribes to server CPU live metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_server_cpu(self, *args: Any, **kwargs: Any) -> None:
        """
        Unsubscribes from server CPU live metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def subscribe_server_ram(self, *args: Any, **kwargs: Any) -> None:
        """
        Subscribes to server RAM live metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_server_ram(self, *args: Any, **kwargs: Any) -> None:
        """
        Unsubscribes from server RAM live metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...
