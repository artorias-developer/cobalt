#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timezone, timedelta
from typing import List, Dict, Callable

from psutil import disk_usage
from orjson import loads

from domain.exceptions import NotFoundError
from application.contracts.clients import AbstractCachesClient
from application.contracts.services import AbstractMetricsService
from application.contracts.mappers import AbstractMetricsServiceMapper
from application.contracts.clients import AbstractMetricsClient
from application.contracts.managers import (
    AbstractConnectionsManager,
    AbstractI18nManager
)
from application.clients.containers.shared import ContainersConstants
from application.managers.connections.shared import RoomsConstants
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    MetricDto,
    MetricDiskDto,
    MetricsSubscribeServerDto,
    MetricsUnsubscribeServerDto
)


class MetricsService(AbstractMetricsService):
    """
    Metrics service.
    """
    caches_client: AbstractCachesClient
    metrics_client: AbstractMetricsClient
    metrics_mapper: AbstractMetricsServiceMapper
    connections_manager: AbstractConnectionsManager
    i18n_manager: AbstractI18nManager

    _: Callable

    def __init__(
        self,
        caches_client: AbstractCachesClient,
        metrics_client: AbstractMetricsClient,
        metrics_mapper: AbstractMetricsServiceMapper,
        connections_manager: AbstractConnectionsManager,
        i18n_manager: AbstractI18nManager
    ):
        self.caches_client = caches_client
        self.metrics_client = metrics_client
        self.metrics_mapper = metrics_mapper
        self.connections_manager = connections_manager
        self.i18n_manager = i18n_manager

        self._ = i18n_manager.gettext

    @staticmethod
    def _get_container_names(
        server_ids: List[int]
    ) -> List[str]:
        """
        Returns a list of container names for the given server IDs.

        Parameters:
        - server_ids: List of server IDs.

        Returns:
        - List: List of container names.
        """
        return [
            ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
                server_id=server_id
            )
            for server_id in server_ids
        ]

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
        if not refresh:
            cached = await self.caches_client.get(
                pattern=CacheConstants.METRICS_HOST_DISK_KEY
            )

            if cached:
                data = loads(cached)
                return MetricDiskDto.from_dict(data)

        disk_data = disk_usage('/')
        now = datetime.now(timezone.utc)

        data = MetricDiskDto(
            free=disk_data.free,
            total=disk_data.total,
            last_check=now,
            next_check=now + timedelta(minutes=5)
        )

        await self.caches_client.set(
            key=CacheConstants.METRICS_HOST_DISK_KEY,
            value=data.model_dump_json(),
            expire=CacheConstants.SHORT_TTL_SECONDS
        )

        return data

    async def host_last_cpu(self) -> MetricDto:
        """
        Gets last host CPU metric value.

        Parameters:
        - None.

        Returns:
        - MetricDto: MetricDto object.
        """
        metric = await self.metrics_client.host_last_cpu()

        if not metric:
            raise NotFoundError(self._("Host CPU metrics not found"))

        return self.metrics_mapper.dataclass_to_dto(
            dataclass=metric
        )

    async def host_last_ram(self) -> MetricDto:
        """
        Gets last host RAM metric value.

        Parameters:
        - None.

        Returns:
        - MetricDto: MetricDto object.
        """
        metric = await self.metrics_client.host_last_ram()

        if not metric:
            raise NotFoundError(self._("Host RAM metrics not found"))

        return self.metrics_mapper.dataclass_to_dto(
            dataclass=metric
        )

    async def host_all_cpu(self) -> List[MetricDto]:
        """
        Gets list of host CPU metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricDto objects.
        """
        metrics = await self.metrics_client.host_all_cpu()

        if not metrics:
            raise NotFoundError(self._("Host CPU metrics not found"))

        return self.metrics_mapper.dataclasses_to_dtos(
            dataclasses=metrics
        )

    async def host_all_ram(self) -> List[MetricDto]:
        """
        Gets list of host RAM metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricDto objects.
        """
        metrics = await self.metrics_client.host_all_ram()

        if not metrics:
            raise NotFoundError(self._("Host RAM metrics not found"))

        return self.metrics_mapper.dataclasses_to_dtos(
            dataclasses=metrics
        )

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
        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        metric = await self.metrics_client.container_last_cpu(
            container=container_name
        )

        if not metric:
            raise NotFoundError(self._("CPU metrics for server {server_id} not found").format(server_id=server_id))

        return self.metrics_mapper.dataclass_to_dto(
            dataclass=metric
        )

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
        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        metric = await self.metrics_client.container_last_ram(
            container=container_name
        )

        if not metric:
            raise NotFoundError(self._("RAM metrics for server {server_id} not found").format(server_id=server_id))

        return self.metrics_mapper.dataclass_to_dto(
            dataclass=metric
        )

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
        container_names = self._get_container_names(
            server_ids=server_ids
        )

        metrics = await self.metrics_client.containers_last_cpu(
            containers=container_names
        )

        if not metrics:
            raise NotFoundError(self._("Servers CPU metrics not found"))

        return {
            name: self.metrics_mapper.dataclass_to_dto(
                dataclass=entity
            )
            for name, entity in metrics.items()
        }

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
        container_names = self._get_container_names(
            server_ids=server_ids
        )

        metrics = await self.metrics_client.containers_last_ram(
            containers=container_names
        )

        if not metrics:
            raise NotFoundError(self._("Servers RAM metrics not found"))

        return {
            name: self.metrics_mapper.dataclass_to_dto(
                dataclass=entity
            )
            for name, entity in metrics.items()
        }

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
        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        metrics = await self.metrics_client.container_all_cpu(
            container=container_name
        )

        if not metrics:
            raise NotFoundError(self._("CPU metrics for server {server_id} not found").format(server_id=server_id))

        return self.metrics_mapper.dataclasses_to_dtos(
            dataclasses=metrics
        )

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
        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        metrics = await self.metrics_client.container_all_ram(
            container=container_name
        )

        if not metrics:
            raise NotFoundError(self._("RAM metrics for server {server_id} not found").format(server_id=server_id))

        return self.metrics_mapper.dataclasses_to_dtos(
            dataclasses=metrics
        )

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
        await self.connections_manager.join_room(
            connection_id=connection_id,
            room_name=RoomsConstants.HOST_CPU_METRICS_KEY,
            metadata={
                "type": "metrics_cpu",
                "target": "host"
            }
        )

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
        await self.connections_manager.leave_room(
            connection_id=connection_id,
            room_name=RoomsConstants.HOST_CPU_METRICS_KEY
        )

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
        await self.connections_manager.join_room(
            connection_id=connection_id,
            room_name=RoomsConstants.HOST_RAM_METRICS_KEY,
            metadata={
                "type": "metrics_ram",
                "target": "host"
            }
        )

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
        await self.connections_manager.leave_room(
            connection_id=connection_id,
            room_name=RoomsConstants.HOST_RAM_METRICS_KEY
        )

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
        room_name = RoomsConstants.SERVER_CPU_METRICS_KEY.format(
            server_id=dto.server_id
        )

        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=dto.server_id
        )

        await self.connections_manager.join_room(
            connection_id=connection_id,
            room_name=room_name,
            metadata={
                "type": "metrics_cpu",
                "target": "server",
                "server_id": dto.server_id,
                "container_name": container_name
            }
        )

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
        room_name = RoomsConstants.SERVER_CPU_METRICS_KEY.format(
            server_id=dto.server_id
        )

        await self.connections_manager.leave_room(
            connection_id=connection_id,
            room_name=room_name
        )

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
        room_name = RoomsConstants.SERVER_RAM_METRICS_KEY.format(
            server_id=dto.server_id
        )

        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=dto.server_id
        )

        await self.connections_manager.join_room(
            connection_id=connection_id,
            room_name=room_name,
            metadata={
                "type": "metrics_ram",
                "target": "server",
                "server_id": dto.server_id,
                "container_name": container_name
            }
        )

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
        room_name = RoomsConstants.SERVER_RAM_METRICS_KEY.format(
            server_id=dto.server_id
        )

        await self.connections_manager.leave_room(
            connection_id=connection_id,
            room_name=room_name
        )
