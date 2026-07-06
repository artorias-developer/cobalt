#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpAttributesRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for attributes-related operations.
    """

    @abstractmethod
    async def get_page(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets a paginated list of attributes.

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
        Gets an existing attribute.

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
        Creates a new attribute.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def create_many(self, *args: Any, **kwargs: Any) -> Any:
        """
        Creates the new attributes.

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
        Updates an existing attribute.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def update_many(self, *args: Any, **kwargs: Any) -> Any:
        """
        Updates an existing attributes.

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
        Deletes an existing attribute.

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
        Deletes an existing attributes.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...
