#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Depends

from domain.enums import PermissionEnum
from application.contracts.managers import (
    AbstractEventsManager,
    AbstractI18nManager
)
from application.contracts.services import (
    AbstractAuthService,
    AbstractServersService
)
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
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        BaseWsRouter.__init__(self, auth_service, i18n_manager)

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
            event=ServersEventsEnum.SUBSCRIBE_STATES,
            handler=self.subscribe_states,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionEnum.SERVERS_VIEW
                    ]
                ))
            ]
        )

        self.events_manager.on_event(
            event=ServersEventsEnum.UNSUBSCRIBE_STATES,
            handler=self.unsubscribe_states,
            dependencies=[
                Depends(self.ws_permission_required(
                    permissions=[
                        PermissionEnum.SERVERS_VIEW
                    ]
                ))
            ]
        )

    async def subscribe_states(
        self,
        connection_id: int
    ) -> None:
        """
        Subscribes to servers states.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        await self.servers_service.subscribe_states(
            connection_id=connection_id
        )

    async def unsubscribe_states(
        self,
        connection_id: int
    ) -> None:
        """
        Unsubscribes from servers states.

        Parameters:
        - connection_id: Connection ID.

        Returns:
        - None.
        """
        await self.servers_service.unsubscribe_states(
            connection_id=connection_id
        )
