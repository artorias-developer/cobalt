#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpMetricsRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for metrics-related operations.
    """

    @abstractmethod
    async def host_disk(
        self,
        refresh: bool = False
    ) -> Any:
        """
        Gets host disk usage metrics.

        Parameters:
        - refresh: If True, bypasses cache and fetches fresh data.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def host_last_cpu(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets last host CPU metric value.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def host_last_ram(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets last host RAM metric value.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def host_all_cpu(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets list of host CPU metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def host_all_ram(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets list of host RAM metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def server_last_cpu(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets last server CPU metric value.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def server_last_ram(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets last server RAM metric value.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def server_all_cpu(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets list of server CPU metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def server_all_ram(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets list of server RAM metrics.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...