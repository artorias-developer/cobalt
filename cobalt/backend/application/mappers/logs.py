#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.contracts.mappers import AbstractLogsServiceMapper
from application.clients.containers.shared import ContainerLog
from application.dtos import LogDto


class LogsServiceMapper(AbstractLogsServiceMapper):
    """
    Mapper for logs service.
    """

    def dataclass_to_dto(
        self,
        dataclass: ContainerLog
    ) -> LogDto:
        """
        Converts ContainerLog object to LogDto object.

        Parameters:
        - dataclass: ContainerLog object.

        Returns:
        - LogDto: LogDto object.
        """
        return LogDto(
            message=dataclass.message
        )

    def dataclasses_to_dtos(
        self,
        dataclasses: List[ContainerLog]
    ) -> List[LogDto]:
        """
        Converts ContainerLog objects to LogDto objects.

        Parameters:
        - dataclasses: List of ContainerLog objects.

        Returns:
        - List: List of LogDto objects.
        """
        return [
            self.dataclass_to_dto(dto)
            for dto in dataclasses
        ]