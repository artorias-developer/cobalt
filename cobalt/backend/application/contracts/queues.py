#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, Callable


class AbstractQueue(ABC):
    """
    Abstract queue.
    """

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initializes the queue.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def enqueue(
        self,
        function: Callable,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        """
        Enqueues a task.

        Parameters:
        - function: Function to execute.
        - args: Positional arguments.
        - kwargs: Keyword arguments.

        Returns:
        - Any: Task result or job ID.
        """
        ...
