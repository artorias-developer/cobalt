#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.dtos import (
    MetricDto,
    MetricDiskDto
)
from presentation.contracts.http.mappers import AbstractMetricsRouterMapper
from presentation.http.fastapi.v1.schemas import (
    MetricSchema,
    MetricDiskSchema
)


class MetricsRouterMapper(AbstractMetricsRouterMapper):
    """
    Mapper for metrics router.
    """

    def dto_to_schema(
        self,
        dto: MetricDto
    ) -> MetricSchema:
        """
        Converts MetricDto object to MetricSchema object.

        Parameters:
        - dto: MetricDto object.

        Returns:
        - MetricSchema: MetricSchema object.
        """
        return MetricSchema(
            value=dto.value,
            date=dto.date
        )

    def disk_dto_to_schema(
        self,
        dto: MetricDiskDto
    ) -> MetricDiskSchema:
        """
        Converts MetricDiskDto object to MetricDiskSchema object.

        Parameters:
        - dto: MetricDiskDto object.

        Returns:
        - MetricDiskSchema: MetricDiskSchema object.
        """
        return MetricDiskSchema(
            free=dto.free,
            total=dto.total,
            last_check=dto.last_check,
            next_check=dto.next_check
        )

    def dtos_to_schemas(
        self,
        dtos: List[MetricDto]
    ) -> List[MetricSchema]:
        """
        Converts MetricDto objects to MetricSchema objects.

        Parameters:
        - dtos: List of MetricDto objects.

        Returns:
        - List: List of MetricSchema objects.
        """
        return [
            self.dto_to_schema(dto)
            for dto in dtos
        ]