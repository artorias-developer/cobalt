#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Depends

from domain.enums import PermissionsEnum
from application.contracts.services import (
    AbstractAuthService,
    AbstractMetricsService
)
from application.contracts.managers import (
    AbstractEventsManager,
    AbstractI18nManager
)
from application.managers.events.shared import MetricsEventsEnum
from application.dtos import (
    MetricsSubscribeServerDto,
    MetricsUnsubscribeServerDto
)
from presentation.contracts.ws.events import AbstractWsMetricsEvents
from presentation.ws.fastapi.v1.routers import BaseWsRouter


class WsMetricsEvents(AbstractWsMetricsEvents, BaseWsRouter):
    """
    Handles WebSockets events for metrics operations.
    """
    router: APIRouter
    events_manager: AbstractEventsManager
    metrics_service: AbstractMetricsService

    def __init__(
        self,
        router: APIRouter,
        events_manager: AbstractEventsManager,
        metrics_service: AbstractMetricsService,
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        BaseWsRouter.__init__(self, auth_service, i18n_manager)

        self.router = router
        self.events_manager = events_manager
        self.metrics_service = metrics_service

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self.events_manager.on_event(
            event=MetricsEventsEnum.SUBSCRIBE_HOST_CPU,
            handler=self.subscribe_host_cpu,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_CPU_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=MetricsEventsEnum.UNSUBSCRIBE_HOST_CPU,
            handler=self.unsubscribe_host_cpu,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_CPU_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=MetricsEventsEnum.SUBSCRIBE_HOST_RAM,
            handler=self.subscribe_host_ram,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_RAM_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=MetricsEventsEnum.UNSUBSCRIBE_HOST_RAM,
            handler=self.unsubscribe_host_ram,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_RAM_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=MetricsEventsEnum.SUBSCRIBE_SERVER_CPU,
            handler=self.subscribe_server_cpu,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_CPU_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=MetricsEventsEnum.UNSUBSCRIBE_SERVER_CPU,
            handler=self.unsubscribe_server_cpu,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_CPU_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=MetricsEventsEnum.SUBSCRIBE_SERVER_RAM,
            handler=self.subscribe_server_ram,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_RAM_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=MetricsEventsEnum.UNSUBSCRIBE_SERVER_RAM,
            handler=self.unsubscribe_server_ram,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_RAM_VIEW
                    ]
                ))
            ]
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
        await self.metrics_service.subscribe_host_cpu(
            connection_id=connection_id
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
        await self.metrics_service.unsubscribe_host_cpu(
            connection_id=connection_id
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
        await self.metrics_service.subscribe_host_ram(
            connection_id=connection_id
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
        await self.metrics_service.unsubscribe_host_ram(
            connection_id=connection_id
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
        await self.metrics_service.subscribe_server_cpu(
            connection_id=connection_id,
            dto=dto
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
        await self.metrics_service.unsubscribe_server_cpu(
            connection_id=connection_id,
            dto=dto
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
        await self.metrics_service.subscribe_server_ram(
            connection_id=connection_id,
            dto=dto
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
        await self.metrics_service.unsubscribe_server_ram(
            connection_id=connection_id,
            dto=dto
        )
