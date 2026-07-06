#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpSettingsRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for settings-related operations.
    """

    @abstractmethod
    async def update_me(self, *args: Any, **kwargs: Any) -> Any:
        """
        Updates settings for the currently authenticated user.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def clear_cache(self, *args: Any, **kwargs: Any) -> Any:
        """
        Clears application cached data.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def clear_containers(self, *args: Any, **kwargs: Any) -> Any:
        """
        Clears unused containers data.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...