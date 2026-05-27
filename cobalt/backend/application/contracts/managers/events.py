#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from application.contracts.interceptors import AbstractInterceptor


class AbstractEventsManager(ABC):
    """
    Abstract events manager.
    """
    _interceptors: List[AbstractInterceptor]
    _event_handlers: Dict[str, Dict[str, Any]]

    def __init__(self):
        self._event_handlers = {}
        self._interceptors = []

    def add_interceptor(
        self,
        interceptor: AbstractInterceptor
    ) -> None:
        """
        Adds the interceptor to the events manager.

        Parameters:
        - interceptor: AbstractInterceptor object.

        Returns:
        - None.
        """
        self._interceptors.append(interceptor)

    @abstractmethod
    async def handler(self, *args: Any, **kwargs: Any) -> Any:
        """
        Handles events.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def on_event(self, *args: Any, **kwargs: Any) -> Any:
        """
        Registers event handler.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def dispatch_event(self, *args: Any, **kwargs: Any) -> Any:
        """
        Calls registered event handler.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...