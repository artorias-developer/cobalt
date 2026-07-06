#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpRolesRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for roles-related operations.
    """

    @abstractmethod
    async def get_page(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets a paginated list of roles.

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
        Gets an existing role.

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
        Creates a new role.

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
        Updates an existing role.

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
        Deletes an existing role.

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
        Deletes multiple existing roles.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...