#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import Depends, APIRouter

from application.contracts.services import AbstractAuthService
from application.contracts.managers import AbstractEventsManager
from presentation.contracts.ws.routers import AbstractWsEventsRouter
from presentation.ws.fastapi.v1.routers import BaseWsRouter


class WsEventsRouter(AbstractWsEventsRouter, BaseWsRouter):
    """
    Handles all WebSockets events.
    """
    router: APIRouter
    events_manager: AbstractEventsManager

    def __init__(
        self,
        router: APIRouter,
        events_manager: AbstractEventsManager,
        auth_service: AbstractAuthService
    ):
        super().__init__(auth_service)

        self.router = router
        self.events_manager = events_manager
        self.event_handlers = {}

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/ws",
            tags=["WebSockets"],
            dependencies=[
                Depends(self.ws_session_required)
            ]
        )

        router.add_api_websocket_route(
            path="",
            name="websocket",
            endpoint=self.events_manager.handler
        )

        self.router.include_router(router)
