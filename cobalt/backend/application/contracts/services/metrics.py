#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import List, Dict

from application.dtos import (
    MetricDto,
    MetricDiskDto,
    MetricsSubscribeServerDto,
    MetricsUnsubscribeServerDto
)


class AbstractMetricsService(ABC):
    """
    Abstract metrics service.
    """

    @abstractmethod
    async def host_disk(
        self,
        refresh: bool = False
    ) -> MetricDiskDto:
        """
        Gets host disk usage metrics.

        Parameters:
        - refresh: If True, bypasses cache and fetches fresh data.

        Returns:
        - MetricDiskDto: MetricDiskDto object.
        """
        ...

    @abstractmethod
    async def host_last_cpu(self) -> MetricDto:
        """
        Gets last host CPU metric value.

        Parameters:
        - None.

        Returns:
        - MetricDto: MetricDto object.
        """
        ...

    @abstractmethod
    async def host_last_ram(self) -> MetricDto:
        """
        Gets last host RAM metric value.

        Parameters:
        - None.

        Returns:
        - MetricDto: MetricDto object.
        """
        ...

    @abstractmethod
    async def host_all_cpu(self) -> List[MetricDto]:
        """
        Gets list of host CPU metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricDto objects.
        """
        ...

    @abstractmethod
    async def host_all_ram(self) -> List[MetricDto]:
        """
        Gets list of host RAM metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricDto objects.
        """
        ...

    @abstractmethod
    async def server_last_cpu(
        self,
        server_id: int
    ) -> MetricDto:
        """
        Gets last server CPU metric value.

        Parameters:
        - server_id: Server ID.

        Returns:
        - MetricDto: MetricDto object.
        """
        ...

    @abstractmethod
    async def server_last_ram(
        self,
        server_id: int
    ) -> MetricDto:
        """
        Gets last server RAM metric value.

        Parameters:
        - server_id: Server ID.

        Returns:
        - MetricDto: MetricDto object.
        """
        ...

    @abstractmethod
    async def servers_last_cpu(
        self,
        server_ids: List[int]
    ) -> Dict[str, MetricDto]:
        """
        Gets last CPU metric value for several servers.

        Parameters:
        - server_ids: List of server IDs.

        Returns:
        - Dict: Dictionary mapping container name to MetricDto.
        """
        ...

    @abstractmethod
    async def servers_last_ram(
        self,
        server_ids: List[int]
    ) -> Dict[str, MetricDto]:
        """
        Gets last RAM metric value for several servers.

        Parameters:
        - server_ids: List of server IDs.

        Returns:
        - Dict: Dictionary mapping container name to MetricDto.
        """
        ...

    @abstractmethod
    async def server_all_cpu(
        self,
        server_id: int
    ) -> List[MetricDto]:
        """
        Gets list of server CPU metrics.

        Parameters:
        - server_id: Server ID.

        Returns:
        - List: List of MetricDto objects.
        """
        ...

    @abstractmethod
    async def server_all_ram(
        self,
        server_id: int
    ) -> List[MetricDto]:
        """
        Gets list of server RAM metrics.

        Parameters:
        - server_id: Server ID.

        Returns:
        - List: List of MetricDto objects.
        """
        ...

    @abstractmethod
    async def subscribe_host_cpu(
        self,
        connection_id: int
    ) -> None:
        """
        Subscribes to host CPU live metrics.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_host_cpu(
        self,
        connection_id: int
    ) -> None:
        """
        Unsubscribes from host CPU live metrics.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def subscribe_host_ram(
        self,
        connection_id: int
    ) -> None:
        """
        Subscribes to host RAM live metrics.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_host_ram(
        self,
        connection_id: int
    ) -> None:
        """
        Unsubscribes from host RAM live metrics.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def subscribe_server_cpu(
        self,
        connection_id: int,
        dto: MetricsSubscribeServerDto
    ) -> None:
        """
        Subscribes to server CPU live metrics.

        Parameters:
        - connection_id: Connection ID.
        - dto: MetricsServerSubscribeDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_server_cpu(
        self,
        connection_id: int,
        dto: MetricsUnsubscribeServerDto
    ) -> None:
        """
        Unsubscribes from server CPU live metrics.

        Parameters:
        - connection_id: Connection ID.
        - dto: MetricsServerUnsubscribeDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def subscribe_server_ram(
        self,
        connection_id: int,
        dto: MetricsSubscribeServerDto
    ) -> None:
        """
        Subscribes to server RAM live metrics.

        Parameters:
        - connection_id: Connection ID.
        - dto: MetricsServerSubscribeDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def unsubscribe_server_ram(
        self,
        connection_id: int,
        dto: MetricsUnsubscribeServerDto
    ) -> None:
        """
        Unsubscribes from server RAM live metrics.

        Parameters:
        - connection_id: Connection ID.
        - dto: MetricsServerUnsubscribeDto object.

        Returns:
        - None.
        """
        ...
