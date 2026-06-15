#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Depends

from domain.enums import PermissionsEnum
from application.contracts.services import (
    AbstractAuthService,
    AbstractServersService
)
from application.contracts.managers import AbstractEventsManager
from application.managers.events.shared import ServersEventsEnum
from presentation.contracts.ws.events import AbstractWsServersEvents
from presentation.ws.fastapi.v1.routers import BaseWsRouter


class WsServersEvents(AbstractWsServersEvents, BaseWsRouter):
    """
    Handles WebSockets events for servers operations.
    """
    router: APIRouter
    events_manager: AbstractEventsManager
    servers_service: AbstractServersService

    def __init__(
        self,
        router: APIRouter,
        events_manager: AbstractEventsManager,
        servers_service: AbstractServersService,
        auth_service: AbstractAuthService
    ):
        BaseWsRouter.__init__(self, auth_service)

        self.router = router
        self.events_manager = events_manager
        self.servers_service = servers_service

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self.events_manager.on_event(
            event=ServersEventsEnum.SUBSCRIBE_STATUSES,
            handler=self.subscribe_statuses,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.SERVERS_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=ServersEventsEnum.UNSUBSCRIBE_STATUSES,
            handler=self.unsubscribe_statuses,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionsEnum.SERVERS_VIEW
                    ]
                ))
            ]
        )

    async def subscribe_statuses(
        self,
        connection_id: int
    ) -> None:
        """
        Subscribes to servers statuses.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        await self.servers_service.subscribe_statuses(
            connection_id=connection_id
        )

    async def unsubscribe_statuses(
        self,
        connection_id: int
    ) -> None:
        """
        Unsubscribes from server statuses.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        await self.servers_service.unsubscribe_statuses(
            connection_id=connection_id
        )
