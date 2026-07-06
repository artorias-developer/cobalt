#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any


class AbstractHttpRouter(ABC):
    """
    Abstract router.
    """

    @abstractmethod
    def register(self, *args: Any, **kwargs: Any) -> None:
        """
        Registers all handlers.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...
