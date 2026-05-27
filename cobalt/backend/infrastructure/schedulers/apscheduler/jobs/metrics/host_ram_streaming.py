#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from domain.exceptions import NotFoundError
from application.contracts.services import AbstractMetricsService
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.loggers import AbstractLogger
from application.managers.connections.shared import RoomsConstants
from application.managers.events.shared import MetricsEventsEnum
from infrastructure.schedulers.apscheduler.jobs import BaseApschedulerJob


class HostRamMetricsStreamingJob(BaseApschedulerJob):
    """
    Job for streaming host RAM live metrics.
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
        Sends last host RAM metric to all subscribers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            metric = await self.metrics_service.host_last_ram()
        except NotFoundError:
            return

        metric_dict = metric.model_dump(mode="json")

        await self.connections_manager.send_to_room(
            room_name=RoomsConstants.HOST_RAM_METRICS_KEY,
            data={
                "type": "message",
                "event": MetricsEventsEnum.HOST_RAM_METRIC,
                "data": metric_dict
            }
        )