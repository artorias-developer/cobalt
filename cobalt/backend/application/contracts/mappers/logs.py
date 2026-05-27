#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List

from application.clients.containers.shared import ContainerLog
from application.dtos import LogDto


class AbstractLogsServiceMapper(ABC):
    """
    Abstract mapper for logs service.
    """

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...