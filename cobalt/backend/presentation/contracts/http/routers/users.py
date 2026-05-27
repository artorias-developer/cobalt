#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpUsersRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for users-related operations.
    """

    @abstractmethod
    async def get_page(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets a paginated list of users.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def get_me(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets the currently authenticated user.

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
        Gets an existing user.

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
        Creates a new user.

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
        Updates an existing user.

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
        Deletes an existing user.

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
        Deletes multiple existing users.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...
