#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from application.dtos import LogDto


class AbstractLogsRouterMapper(ABC):
    """
    Abstract mapper for logs router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: LogDto
    ) -> Any:
        """
        Converts LogDto object to schema object.

        Parameters:
        - dto: LogDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def dtos_to_schemas(
        self,
        dtos: List[LogDto]
    ) -> List[Any]:
        """
        Converts LogDto objects to schema objects.

        Parameters:
        - dtos: List of LogDto objects.

        Returns:
        - List: List of any schema objects.
        """
        ...
