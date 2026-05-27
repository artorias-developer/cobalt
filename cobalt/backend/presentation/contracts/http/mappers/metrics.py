#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from application.dtos import (
    MetricDto,
    MetricDiskDto
)


class AbstractMetricsRouterMapper(ABC):
    """
    Abstract mapper for metrics router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: MetricDto
    ) -> Any:
        """
        Converts MetricDto object to schema object.

        Parameters:
        - dto: MetricDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def disk_dto_to_schema(
        self,
        dto: MetricDiskDto
    ) -> Any:
        """
        Converts MetricDiskDto object to schema object.

        Parameters:
        - dto: MetricDiskDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def dtos_to_schemas(
        self,
        dtos: List[MetricDto]
    ) -> List[Any]:
        """
        Converts MetricDto objects to schema objects.

        Parameters:
        - dtos: List of MetricDto objects.

        Returns:
        - List: List of any schema objects.
        """
        ...