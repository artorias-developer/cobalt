#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpServersRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for servers-related operations.
    """

    @abstractmethod
    async def get_page(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets a paginated list of servers.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def get_one(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets an existing server.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def create_one(self, *args: Any, **kwargs: Any) -> Any:
        """
        Creates a new server.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def update_one(self, *args: Any, **kwargs: Any) -> Any:
        """
        Updates an existing server.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def delete_one(self, *args: Any, **kwargs: Any) -> Any:
        """
        Deletes an existing server.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def delete_many(self, *args: Any, **kwargs: Any) -> Any:
        """
        Deletes multiple existing servers.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def start(self, *args: Any, **kwargs: Any) -> Any:
        """
        Starts an existing server.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def stop(self, *args: Any, **kwargs: Any) -> Any:
        """
        Stops an existing server.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Executes a command inside the server container.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def status(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets the server container status.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...