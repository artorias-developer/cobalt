#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpLogsRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for logs-related operations.
    """

    @abstractmethod
    async def host_all(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets a list of all host logs.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def server_all(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets a list of all server logs.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...