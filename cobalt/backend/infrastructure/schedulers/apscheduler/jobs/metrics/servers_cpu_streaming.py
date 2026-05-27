#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from domain.exceptions import NotFoundError
from application.contracts.services import AbstractMetricsService
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.loggers import AbstractLogger
from application.managers.events.shared import MetricsEventsEnum
from infrastructure.schedulers.apscheduler.jobs import BaseApschedulerJob


class ServersCpuMetricsStreamingJob(BaseApschedulerJob):
    """
    Job for streaming servers CPU live metrics.
    """
    metrics_service: AbstractMetricsService
    connections_manager: AbstractConnectionsManager

    def __init__(
        self,
        metrics_service: AbstractMetricsService,
        connections_manager: AbstractConnectionsManager,
        logger: AbstractLogger
    ):
        super().__init__(logger)

        self.metrics_service = metrics_service
        self.connections_manager = connections_manager

    async def execute(self) -> None:
        """
        Sends last server CPU metrics to all subscribers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        server_ids = []
        container_to_room = {}

        rooms = await self.connections_manager.find_rooms_by_metadata(
            type="metrics_cpu",
            target="server"
        )

        for room_name, room in rooms:
            if not room.connections:
                continue

            server_id = room.metadata.get("server_id")
            container_name = room.metadata.get("container_name")

            server_ids.append(server_id)
            container_to_room[container_name] = (room_name, server_id)

        if not server_ids:
            return

        try:
            metrics = await self.metrics_service.servers_last_cpu(
                server_ids=server_ids
            )
        except NotFoundError:
            return

        for container_name, metric in metrics.items():
            room_data = container_to_room.get(container_name)

            if not room_data:
                continue

            room_name, server_id = room_data

            await self.connections_manager.send_to_room(
                room_name=room_name,
                data={
                    "type": "message",
                    "event": MetricsEventsEnum.SERVER_CPU_METRIC,
                    "server_id": server_id,
                    "data": metric.model_dump(mode="json")
                }
            )