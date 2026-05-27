#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List

from application.clients.metrics.shared import MetricPoint
from application.dtos import MetricDto


class AbstractMetricsServiceMapper(ABC):
    """
    Abstract mapper for metrics service.
    """

    @abstractmethod
    def dataclass_to_dto(
        self,
        dataclass: MetricPoint
    ) -> MetricDto:
        """
        Converts MetricPoint object to MetricDto object.

        Parameters:
        - dataclass: MetricPoint object.

        Returns:
        - MetricDto: MetricDto object.
        """
        ...

    @abstractmethod
    def dataclasses_to_dtos(
        self,
        dataclasses: List[MetricPoint]
    ) -> List[MetricDto]:
        """
        Converts MetricPoint objects to MetricDto objects.

        Parameters:
        - dataclasses: List of MetricPoint objects.

        Returns:
        - List: List of MetricDto objects.
        """
        ...