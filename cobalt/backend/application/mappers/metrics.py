#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.contracts.mappers import AbstractMetricsServiceMapper
from application.clients.metrics.shared import MetricPoint
from application.dtos import MetricDto


class MetricsServiceMapper(AbstractMetricsServiceMapper):
    """
    Mapper for metrics service.
    """
    
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
        return MetricDto(
            value=dataclass.value,
            date=dataclass.date
        )

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
        return [
            self.dataclass_to_dto(entity)
            for entity in dataclasses
        ]
