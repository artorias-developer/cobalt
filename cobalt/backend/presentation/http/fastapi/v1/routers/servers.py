#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Response, status, Depends, Body

from domain.enums import PermissionEnum
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import (
    AbstractServersService,
    AbstractAuthService
)
from presentation.contracts.http.routers import AbstractHttpServersRouter
from presentation.contracts.http.mappers import AbstractServersRouterMapper
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import (
    ServerSchema,
    ServersGetPageSchema,
    ServersPageSchema,
    ServerCreateSchema,
    ServerUpdateSchema,
    ServersDeleteSchema,
    ServerExecuteSchema,
    ServerStatusSchema
)


class HttpServersRouter(AbstractHttpServersRouter, HttpBaseRouter):
    """
    Handles HTTP routes for servers operations.
    """
    router: APIRouter
    servers_service: AbstractServersService
    servers_mapper: AbstractServersRouterMapper

    def __init__(
        self,
        router: APIRouter,
        servers_service: AbstractServersService,
        servers_mapper: AbstractServersRouterMapper,
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        HttpBaseRouter.__init__(self, auth_service, i18n_manager)

        self.router = router
        self.servers_service = servers_service
        self.servers_mapper = servers_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/servers",
            tags=["Servers"],
            dependencies=[
                Depends(self.http_session_required)
            ]
        )

        router.add_api_route(
            path="/batch",
            endpoint=self.delete_many,
            methods=["DELETE"],
            operation_id="servers_delete_many",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVERS_DELETE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.get_page,
            methods=["GET"],
            operation_id="servers_get_page",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVERS_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{server_id}",
            endpoint=self.get_one,
            methods=["GET"],
            operation_id="servers_get_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVERS_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.create_one,
            methods=["POST"],
            operation_id="servers_create_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVERS_CREATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{server_id}",
            endpoint=self.update_one,
            methods=["PATCH"],
            operation_id="servers_update_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVER_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{server_id}",
            endpoint=self.delete_one,
            methods=["DELETE"],
            operation_id="servers_delete_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVERS_DELETE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{server_id}/start",
            endpoint=self.start,
            methods=["POST"],
            operation_id="servers_start",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVER_START
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{server_id}/stop",
            endpoint=self.stop,
            methods=["POST"],
            operation_id="servers_stop",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVER_STOP
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{server_id}/restart",
            endpoint=self.restart,
            methods=["POST"],
            operation_id="servers_restart",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVER_START
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{server_id}/execute",
            endpoint=self.execute,
            methods=["POST"],
            operation_id="servers_execute",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVER_CONSOLE_EXECUTE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{server_id}/status",
            endpoint=self.status,
            methods=["GET"],
            operation_id="servers_status",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionEnum.SERVER_VIEW
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def get_page(
        self,
        schema: ServersGetPageSchema = Depends()
    ) -> ServersPageSchema:
        """
        Gets a paginated list of servers.

        Parameters:
        - schema: ServersGetPageSchema object.

        Returns:
        - ServersPageSchema: ServersPageSchema object.
        """
        request_dto = self.servers_mapper.get_page_schema_to_dto(
            schema=schema
        )

        response_dto = await self.servers_service.get_page(
            dto=request_dto
        )

        return self.servers_mapper.page_dto_to_schema(
            dto=response_dto
        )

    async def get_one(
        self,
        server_id: int
    ) -> ServerSchema:
        """
        Gets an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - ServerSchema: ServerSchema object.
        """
        response_dto = await self.servers_service.get_one_by_id(
            server_id=server_id
        )

        return self.servers_mapper.dto_to_schema(
            dto=response_dto
        )

    async def create_one(
        self,
        schema: ServerCreateSchema = Body(...)
    ) -> ServerSchema:
        """
        Creates a new server.

        Parameters:
        - schema: ServerCreateSchema object.

        Returns:
        - ServerSchema: ServerSchema object.
        """
        request_dto = self.servers_mapper.create_schema_to_dto(
            schema=schema
        )

        response_dto = await self.servers_service.create_one(
            dto=request_dto
        )

        return self.servers_mapper.dto_to_schema(
            dto=response_dto
        )

    async def update_one(
        self,
        server_id: int,
        schema: ServerUpdateSchema = Body(...)
    ) -> ServerSchema:
        """
        Updates an existing server.

        Parameters:
        - server_id: Server ID.
        - schema: ServerUpdateSchema object.

        Returns:
        - ServerSchema: ServerSchema object.
        """
        request_dto = self.servers_mapper.update_schema_to_dto(
            schema=schema
        )

        response_dto = await self.servers_service.update_one(
            server_id=server_id,
            dto=request_dto
        )

        return self.servers_mapper.dto_to_schema(
            dto=response_dto
        )

    async def delete_one(
        self,
        server_id: int
    ) -> Response:
        """
        Deletes an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - Response: Response object.
        """
        await self.servers_service.delete_one(
            server_id=server_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def delete_many(
        self,
        schema: ServersDeleteSchema = Body(...)
    ) -> Response:
        """
        Deletes multiple existing servers.

        Parameters:
        - schema: ServersDeleteSchema object.

        Returns:
        - Response: Response object.
        """
        await self.servers_service.delete_many(
            server_ids=schema.root
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def start(
        self,
        server_id: int
    ) -> Response:
        """
        Starts an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - Response: Response object.
        """
        await self.servers_service.start(
            server_id=server_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def stop(
        self,
        server_id: int
    ) -> Response:
        """
        Stops an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - Response: Response object.
        """
        await self.servers_service.stop(
            server_id=server_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def restart(
        self,
        server_id: int
    ) -> Response:
        """
        Restarts an existing server.

        Parameters:
        - server_id: Server ID.

        Returns:
        - Response: Response object.
        """
        await self.servers_service.restart(
            server_id=server_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def execute(
        self,
        server_id: int,
        schema: ServerExecuteSchema = Body(...)
    ) -> Response:
        """
        Executes a command inside the server container.

        Parameters:
        - server_id: Server ID.
        - schema: ServerExecuteSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.servers_mapper.execute_schema_to_dto(
            schema=schema
        )

        await self.servers_service.execute(
            server_id=server_id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def status(
        self,
        server_id: int
    ) -> ServerStatusSchema:
        """
        Gets the server container status.

        Parameters:
        - server_id: Server ID.

        Returns:
        - ServerStatusSchema: ServerStatusSchema object.
        """
        response_dto = await self.servers_service.status(
            server_id=server_id
        )

        return self.servers_mapper.status_dto_to_schema(
            dto=response_dto
        )