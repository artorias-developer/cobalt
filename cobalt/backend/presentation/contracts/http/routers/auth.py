#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpAuthRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for auth-related operations.
    """

    @abstractmethod
    async def login(self, *args: Any, **kwargs: Any) -> Any:
        """
        Authenticates a user and creates a session.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def logout(self, *args: Any, **kwargs: Any) -> Any:
        """
        Deletes the user's session.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def change_credentials(self, *args: Any, **kwargs: Any) -> Any:
        """
        Changes login and/or password for the currently authenticated user.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

