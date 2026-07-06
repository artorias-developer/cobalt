#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, List, Dict

from application.clients.metrics.shared import MetricPoint


class AbstractMetricsClient(ABC):
    """
    Abstract metrics client.
    """

    @abstractmethod
    async def host_last_cpu(self) -> Optional[MetricPoint]:
        """
        Gets last host CPU metric value.

        Parameters:
        - None.

        Returns:
        - MetricPoint: MetricPoint object.
        """
        ...

    @abstractmethod
    async def host_last_ram(self) -> Optional[MetricPoint]:
        """
        Gets last host RAM metric value.

        Parameters:
        - None.

        Returns:
        - MetricPoint: MetricPoint object.
        """
        ...

    @abstractmethod
    async def host_all_cpu(self) -> List[MetricPoint]:
        """
        Gets list of host CPU metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricPoint objects.
        """
        ...

    @abstractmethod
    async def host_all_ram(self) -> List[MetricPoint]:
        """
        Gets list of host RAM metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricPoint objects.
        """
        ...

    @abstractmethod
    async def container_last_cpu(
        self,
        container: str
    ) -> Optional[MetricPoint]:
        """
        Gets last container CPU metric value.

        Parameters:
        - container: Container name.

        Returns:
        - MetricPoint: MetricPoint object.
        """
        ...

    @abstractmethod
    async def container_last_ram(
        self,
        container: str
    ) -> Optional[MetricPoint]:
        """
        Gets last container RAM metric value.

        Parameters:
        - container: Container name.

        Returns:
        - MetricPoint: MetricPoint object.
        """
        ...

    @abstractmethod
    async def container_all_cpu(
        self,
        container: str
    ) -> List[MetricPoint]:
        """
        Gets list of container CPU metrics.

        Parameters:
        - container: Container name.

        Returns:
        - List: List of MetricPoint objects.
        """
        ...

    @abstractmethod
    async def container_all_ram(
        self,
        container: str
    ) -> List[MetricPoint]:
        """
        Gets list of container RAM metrics.

        Parameters:
        - container: Container name.

        Returns:
        - List: List of MetricPoint objects.
        """
        ...

    @abstractmethod
    async def containers_last_cpu(
        self,
        containers: List[str]
    ) -> Dict[str, MetricPoint]:
        """
        Gets last CPU metrics for multiple containers.

        Parameters:
        - containers: List of container names.

        Returns:
        - Dict: Dictionary mapping container name to MetricPoint.
        """
        ...

    @abstractmethod
    async def containers_last_ram(
        self,
        containers: List[str]
    ) -> Dict[str, MetricPoint]:
        """
        Gets last RAM metrics for multiple containers.

        Parameters:
        - containers: List of container names.

        Returns:
        - Dict: Dictionary mapping container name to MetricPoint.
        """
        ...