#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Depends

from domain.enums import PermissionEnum
from application.contracts.services import (
    AbstractAuthService,
    AbstractLogsService
)
from application.contracts.managers import (
    AbstractEventsManager,
    AbstractI18nManager
)
from application.managers.events.shared import LogsEventsEnum
from application.dtos import (
    LogsSubscribeServerDto,
    LogsUnsubscribeServerDto
)
from presentation.contracts.ws.events import AbstractWsLogsEvents
from presentation.ws.fastapi.v1.routers import BaseWsRouter


class WsLogsEvents(AbstractWsLogsEvents, BaseWsRouter):
    """
    Handles WebSockets events for logs operations.
    """
    router: APIRouter
    events_manager: AbstractEventsManager
    logs_service: AbstractLogsService

    def __init__(
        self,
        router: APIRouter,
        events_manager: AbstractEventsManager,
        logs_service: AbstractLogsService,
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        BaseWsRouter.__init__(self, auth_service, i18n_manager)

        self.router = router
        self.events_manager = events_manager
        self.logs_service = logs_service

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self.events_manager.on_event(
            event=LogsEventsEnum.SUBSCRIBE_HOST,
            handler=self.subscribe_host,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionEnum.DASHBOARD_LOGS_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=LogsEventsEnum.SUBSCRIBE_SERVER,
            handler=self.subscribe_server,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionEnum.SERVER_LOGS_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=LogsEventsEnum.UNSUBSCRIBE_HOST,
            handler=self.unsubscribe_host,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionEnum.DASHBOARD_LOGS_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=LogsEventsEnum.UNSUBSCRIBE_SERVER,
            handler=self.unsubscribe_server,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionEnum.SERVER_LOGS_VIEW
                    ]
                ))
            ]
        )

    async def subscribe_host(
        self,
        connection_id: int
    ) -> None:
        """
        Subscribes to host live logs.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        await self.logs_service.subscribe_host(
            connection_id=connection_id
        )

    async def subscribe_server(
        self,
        connection_id: int,
        dto: LogsSubscribeServerDto
    ) -> None:
        """
        Subscribes to server live logs.

        Parameters:
        - connection_id: Connection ID.
        - dto: LogsSubscribeServerDto object.

        Returns:
        - None.
        """
        await self.logs_service.subscribe_server(
            connection_id=connection_id,
            dto=dto
        )

    async def unsubscribe_host(
        self,
        connection_id: int
    ) -> None:
        """
        Unsubscribes from host live logs.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        await self.logs_service.unsubscribe_host(
            connection_id=connection_id
        )

    async def unsubscribe_server(
        self,
        connection_id: int,
        dto: LogsUnsubscribeServerDto
    ) -> None:
        """
         Unsubscribes from server live logs.

        Parameters:
        - connection_id: Connection ID.
        - dto: LogsUnsubscribeServerDto object.

        Returns:
        - None.
        """
        await self.logs_service.unsubscribe_server(
            connection_id=connection_id,
            dto=dto
        )
