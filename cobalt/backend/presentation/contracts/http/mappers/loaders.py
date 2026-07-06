#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from application.dtos import LoaderDto


class AbstractLoadersRouterMapper(ABC):
    """
    Abstract mapper for loaders router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: LoaderDto
    ) -> Any:
        """
        Converts LoaderDto object to schema object.

        Parameters:
        - dto: LoaderDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def dtos_to_schemas(
        self,
        dtos: List[LoaderDto]
    ) -> List[Any]:
        """
        Converts LoaderDto objects to schema objects.

        Parameters:
        - dtos: List of LoaderDto objects.

        Returns:
        - List: List of any schema objects.
        """
        ...

    @abstractmethod
    def dto_to_short_schema(
        self,
        dto: LoaderDto
    ) -> Any:
        """
        Converts LoaderDto object to short schema object.

        Parameters:
        - dto: LoaderDto object.

        Returns:
        - Any: Server schema object.
        """
        ...
