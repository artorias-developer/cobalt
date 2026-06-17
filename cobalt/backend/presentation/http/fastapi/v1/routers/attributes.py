#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from fastapi import APIRouter, Response, status, Depends, Body

from domain.enums import PermissionsEnum
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import (
    AbstractAttributesService,
    AbstractAuthService
)
from presentation.contracts.http.routers import AbstractHttpAttributesRouter
from presentation.contracts.http.mappers import AbstractAttributesRouterMapper
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import (
    AttributeSchema,
    AttributesGetPageSchema,
    AttributesPageSchema,
    AttributeCreateSchema,
    AttributeUpdateSchema,
    AttributesUpdateSchema,
    AttributesDeleteSchema
)


class HttpAttributesRouter(AbstractHttpAttributesRouter, HttpBaseRouter):
    """
    Handles HTTP routes for attributes operations.
    """
    router: APIRouter
    attributes_service: AbstractAttributesService
    attributes_mapper: AbstractAttributesRouterMapper

    def __init__(
        self,
        router: APIRouter,
        attributes_service: AbstractAttributesService,
        attributes_mapper: AbstractAttributesRouterMapper,
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        HttpBaseRouter.__init__(self, auth_service, i18n_manager)

        self.router = router
        self.attributes_service = attributes_service
        self.attributes_mapper = attributes_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/servers/{server_id}/attributes",
            tags=["Attributes"],
            dependencies=[
                Depends(self.http_session_required)
            ]
        )

        router.add_api_route(
            path="/batch",
            endpoint=self.create_many,
            methods=["POST"],
            operation_id="attributes_create_many",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_SETTINGS_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/batch",
            endpoint=self.update_many,
            methods=["PATCH"],
            operation_id="attributes_update_many",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_SETTINGS_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/batch",
            endpoint=self.delete_many,
            methods=["DELETE"],
            operation_id="attributes_delete_many",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_SETTINGS_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.get_page,
            methods=["GET"],
            operation_id="attributes_get_page",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_SETTINGS_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{attribute_id}",
            endpoint=self.get_one,
            methods=["GET"],
            operation_id="attributes_get_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_SETTINGS_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.create_one,
            methods=["POST"],
            operation_id="attributes_create_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_SETTINGS_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{attribute_id}",
            endpoint=self.update_one,
            methods=["PATCH"],
            operation_id="attributes_update_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_SETTINGS_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{attribute_id}",
            endpoint=self.delete_one,
            methods=["DELETE"],
            operation_id="attributes_delete_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_SETTINGS_UPDATE
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def get_page(
        self,
        server_id: int,
        schema: AttributesGetPageSchema = Depends()
    ) -> AttributesPageSchema:
        """
        Gets a paginated list of attributes.

        Parameters:
        - server_id: Server ID.
        - schema: AttributesGetPageSchema object.

        Returns:
        - AttributesPageSchema: AttributesPageSchema object.
        """
        request_dto = self.attributes_mapper.get_page_schema_to_dto(
            schema=schema
        )

        response_dto = await self.attributes_service.get_page(
            server_id=server_id,
            dto=request_dto
        )

        return self.attributes_mapper.page_dto_to_schema(
            dto=response_dto
        )

    async def get_one(
        self,
        server_id: int,
        attribute_id: int
    ) -> AttributeSchema:
        """
        Gets an existing attribute.

        Parameters:
        - server_id: Server ID.
        - attribute_id: Attribute ID.

        Returns:
        - AttributeSchema: AttributeSchema object.
        """
        response_dto = await self.attributes_service.get_one_by_id(
            server_id=server_id,
            attribute_id=attribute_id
        )

        return self.attributes_mapper.dto_to_schema(
            dto=response_dto
        )

    async def create_one(
        self,
        server_id: int,
        schema: AttributeCreateSchema = Body(...)
    ) -> AttributeSchema:
        """
        Creates a new attribute.

        Parameters:
        - server_id: Server ID.
        - schema: AttributeCreateSchema objects.

        Returns:
        - AttributeSchema: AttributeSchema object.
        """
        request_dto = self.attributes_mapper.create_schema_to_dto(
            schema=schema
        )

        response_dto = await self.attributes_service.create_one(
            server_id=server_id,
            dto=request_dto
        )

        return self.attributes_mapper.dto_to_schema(
            dto=response_dto
        )

    async def create_many(
        self,
        server_id: int,
        schemas: List[AttributeCreateSchema] = Body(...)
    ) -> List[AttributeSchema]:
        """
        Creates the new attributes.

        Parameters:
        - server_id: Server ID.
        - schemas: List of AttributeCreateSchema objects.

        Returns:
        - List: List of AttributeSchema objects.
        """
        request_dtos = self.attributes_mapper.create_schemas_to_dtos(
            schemas=schemas
        )

        response_dtos = await self.attributes_service.create_many(
            server_id=server_id,
            dtos=request_dtos
        )

        return self.attributes_mapper.dtos_to_schemas(
            dtos=response_dtos
        )

    async def update_one(
        self,
        server_id: int,
        attribute_id: int,
        schema: AttributeUpdateSchema = Body(...)
    ) -> AttributeSchema:
        """
        Updates an existing attribute.

        Parameters:
        - server_id: Server ID.
        - attribute_id: Attribute ID.
        - schema: AttributeUpdateSchema object.

        Returns:
        - AttributeSchema: AttributeSchema object.
        """
        request_dto = self.attributes_mapper.update_schema_to_dto(
            attribute_id=attribute_id,
            schema=schema
        )

        response_dto = await self.attributes_service.update_one(
            server_id=server_id,
            dto=request_dto
        )

        return self.attributes_mapper.dto_to_schema(
            dto=response_dto
        )

    async def update_many(
        self,
        server_id: int,
        schemas: List[AttributesUpdateSchema] = Body(...)
    ) -> List[AttributeSchema]:
        """
        Updates an existing attributes.

        Parameters:
        - server_id: Server ID.
        - schemas: List of AttributesUpdateSchema objects.

        Returns:
        - List: List of AttributeSchema objects.
        """
        request_dtos = self.attributes_mapper.update_schemas_to_dtos(
            schemas=schemas
        )

        response_dtos = await self.attributes_service.update_many(
            server_id=server_id,
            dtos=request_dtos
        )

        return self.attributes_mapper.dtos_to_schemas(
            dtos=response_dtos
        )

    async def delete_one(
        self,
        server_id: int,
        attribute_id: int
    ) -> Response:
        """
        Deletes an existing attribute.

        Parameters:
        - server_id: Server ID.
        - attribute_id: Attribute ID.

        Returns:
        - Response: Response object.
        """
        await self.attributes_service.delete_one(
            server_id=server_id,
            attribute_id=attribute_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def delete_many(
        self,
        server_id: int,
        schema: AttributesDeleteSchema = Body(...)
    ) -> Response:
        """
        Deletes an existing attributes.

        Parameters:
        - server_id: Server ID.
        - schema: AttributesDeleteSchema object.

        Returns:
        - Response: Response object.
        """
        await self.attributes_service.delete_many(
            server_id=server_id,
            attribute_ids=schema.root
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )