#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Response, status, Depends, Body

from domain.enums import PermissionsEnum
from application.contracts.services import (
    AbstractRolesService,
    AbstractAuthService
)
from presentation.contracts.http.routers import AbstractHttpRolesRouter
from presentation.contracts.http.mappers import AbstractRolesRouterMapper
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import (
    RoleSchema,
    RolesGetPageSchema,
    RolesPageSchema,
    RoleCreateSchema,
    RoleUpdateSchema,
    RolesDeleteSchema
)


class HttpRolesRouter(AbstractHttpRolesRouter, HttpBaseRouter):
    """
    Handles HTTP routes for roles operations.
    """
    router: APIRouter
    roles_service: AbstractRolesService
    roles_mapper: AbstractRolesRouterMapper

    def __init__(
        self,
        router: APIRouter,
        roles_service: AbstractRolesService,
        roles_mapper: AbstractRolesRouterMapper,
        auth_service: AbstractAuthService
    ):
        HttpBaseRouter.__init__(self, auth_service)

        self.router = router
        self.roles_service = roles_service
        self.roles_mapper = roles_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/roles",
            tags=["Roles"],
            dependencies=[
                Depends(self.http_session_required)
            ]
        )

        router.add_api_route(
            path="/batch",
            endpoint=self.delete_many,
            methods=["DELETE"],
            operation_id="roles_delete_many",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.ROLES_DELETE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.get_page,
            methods=["GET"],
            operation_id="roles_get_page",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.ROLES_VIEW,
                        PermissionsEnum.USERS_CREATE,
                        PermissionsEnum.USERS_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{role_id}",
            endpoint=self.get_one,
            methods=["GET"],
            operation_id="roles_get_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.ROLES_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.create_one,
            methods=["POST"],
            operation_id="roles_create_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.ROLES_CREATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{role_id}",
            endpoint=self.update_one,
            methods=["PATCH"],
            operation_id="roles_update_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.ROLES_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{role_id}",
            endpoint=self.delete_one,
            methods=["DELETE"],
            operation_id="roles_delete_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.ROLES_DELETE
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def get_page(
        self,
        schema: RolesGetPageSchema = Depends()
    ) -> RolesPageSchema:
        """
        Gets a paginated list of roles.

        Parameters:
        - schema: RolesGetPageSchema object.

        Returns:
        - RolesPageSchema: RolesPageSchema object.
        """
        request_dto = self.roles_mapper.get_page_schema_to_dto(
            schema=schema
        )

        response_dto = await self.roles_service.get_page(
            dto=request_dto
        )

        return self.roles_mapper.page_dto_to_schema(
            dto=response_dto
        )

    async def get_one(
        self,
        role_id: int
    ) -> RoleSchema:
        """
        Gets an existing role.

        Parameters:
        - role_id: Role ID.

        Returns:
        - RoleSchema: RoleSchema object.
        """
        response_dto = await self.roles_service.get_one_by_id(
            role_id=role_id
        )

        return self.roles_mapper.dto_to_schema(
            dto=response_dto
        )

    async def create_one(
        self,
        schema: RoleCreateSchema = Body(...)
    ) -> RoleSchema:
        """
        Creates a new role.

        Parameters:
        - schema: RoleCreateSchema object.

        Returns:
        - RoleSchema: RoleSchema object.
        """
        request_dto = self.roles_mapper.create_schema_to_dto(
            schema=schema
        )

        response_dto = await self.roles_service.create_one(
            dto=request_dto
        )

        return self.roles_mapper.dto_to_schema(
            dto=response_dto
        )

    async def update_one(
        self,
        role_id: int,
        schema: RoleUpdateSchema = Body(...)
    ) -> RoleSchema:
        """
        Updates an existing role.

        Parameters:
        - role_id: Role ID.
        - schema: RoleUpdateSchema object.

        Returns:
        - RoleSchema: RoleSchema object.
        """
        request_dto = self.roles_mapper.update_schema_to_dto(
            schema=schema
        )

        response_dto = await self.roles_service.update_one(
            role_id=role_id,
            dto=request_dto
        )

        return self.roles_mapper.dto_to_schema(
            dto=response_dto
        )

    async def delete_one(
        self,
        role_id: int
    ) -> Response:
        """
        Deletes an existing role.

        Parameters:
        - role_id: Role ID.

        Returns:
        - Response: Response object.
        """
        await self.roles_service.delete_one(
            role_id=role_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def delete_many(
        self,
        schema: RolesDeleteSchema = Body(...)
    ) -> Response:
        """
        Deletes multiple existing roles.

        Parameters:
        - schema: RolesDeleteSchema object.

        Returns:
        - Response: Response object.
        """
        await self.roles_service.delete_many(
            role_ids=schema.root
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )