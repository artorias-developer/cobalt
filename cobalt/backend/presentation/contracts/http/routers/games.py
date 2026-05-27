#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpGamesRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for games-related operations.
    """

    @abstractmethod
    async def get_page(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets a paginated list of games.

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
        Gets an existing game by ID.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...