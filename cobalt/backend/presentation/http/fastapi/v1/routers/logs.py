#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from fastapi import APIRouter, Depends

from domain.enums import PermissionsEnum
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import (
    AbstractAuthService,
    AbstractLogsService
)
from presentation.contracts.http.mappers import AbstractLogsRouterMapper
from presentation.contracts.http.routers import AbstractHttpLogsRouter
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import LogSchema


class HttpLogsRouter(AbstractHttpLogsRouter, HttpBaseRouter):
    """
    Handles HTTP routes for logs operations.
    """
    router: APIRouter
    logs_service: AbstractLogsService
    logs_mapper: AbstractLogsRouterMapper

    def __init__(
        self,
        router: APIRouter,
        logs_service: AbstractLogsService,
        logs_mapper: AbstractLogsRouterMapper,
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        HttpBaseRouter.__init__(self, auth_service, i18n_manager)

        self.router = router
        self.logs_service = logs_service
        self.logs_mapper = logs_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/logs",
            tags=["Logs"],
            dependencies=[
                Depends(self.http_session_required)
            ]
        )

        router.add_api_route(
            path="/host",
            endpoint=self.host_all,
            methods=["GET"],
            operation_id="logs_host_all",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_LOGS_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/servers/{server_id}",
            endpoint=self.server_all,
            methods=["GET"],
            operation_id="logs_server_all",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_LOGS_VIEW
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def host_all(self) -> List[LogSchema]:
        """
        Gets a list of all host logs.

        Parameters:
        - None.

        Returns:
        - List: List of LogSchema objects.
        """
        response_dtos = await self.logs_service.host_all()

        return self.logs_mapper.dtos_to_schemas(
            dtos=response_dtos
        )

    async def server_all(
        self,
        server_id: int
    ) -> List[LogSchema]:
        """
        Gets a list of all server logs.

        Parameters:
        - server_id: Server ID.

        Returns:
        - List: List of LogSchema objects.
        """
        response_dtos = await self.logs_service.server_all(
            server_id=server_id
        )

        return self.logs_mapper.dtos_to_schemas(
            dtos=response_dtos
        )
