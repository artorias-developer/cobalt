#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.ws.routers import AbstractWsRouter


class AbstractWsServersEvents(AbstractWsRouter, ABC):
    """
    Abstract WebSockets events for status-related operations.
    """

    @abstractmethod
    async def subscribe_states(self, *args: Any, **kwargs: Any) -> None:
        """
        Subscribes to servers states.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_states(self, *args: Any, **kwargs: Any) -> None:
        """
        Unsubscribes from servers states.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...
