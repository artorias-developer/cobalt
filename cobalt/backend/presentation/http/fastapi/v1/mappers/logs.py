#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.dtos import LogDto
from presentation.contracts.http.mappers import AbstractLogsRouterMapper
from presentation.http.fastapi.v1.schemas import LogSchema


class LogsRouterMapper(AbstractLogsRouterMapper):
    """
    Mapper for logs router.
    """

    def dto_to_schema(
        self,
        dto: LogDto
    ) -> LogSchema:
        """
        Converts LogDto object to LogSchema object.

        Parameters:
        - dto: LogDto object.

        Returns:
        - LogSchema: LogSchema object.
        """
        return LogSchema(
            message=dto.message
        )

    def dtos_to_schemas(
        self,
        dtos: List[LogDto]
    ) -> List[LogSchema]:
        """
        Converts LogDto objects to LogSchema objects.

        Parameters:
        - dtos: List of LogDto objects.

        Returns:
        - List: List of LogSchema objects.
        """
        return [
            self.dto_to_schema(dto)
            for dto in dtos
        ]
