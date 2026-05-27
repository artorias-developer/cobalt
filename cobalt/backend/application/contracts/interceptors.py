#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, Callable


class AbstractInterceptor(ABC):
    """
    Abstract interceptor.
    """

    @abstractmethod
    async def dispatch(
        self,
        call_next: Callable,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Wraps handler with additional logic.

        Parameters:
        - call_next: Async callable that processes the next handler in chain.
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...
