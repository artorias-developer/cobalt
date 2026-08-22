#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Request, Response, Depends, Body, status
from starlette.responses import JSONResponse

from domain.enums import PermissionEnum
from application.contracts.services import (
    AbstractSettingsService,
    AbstractAuthService
)
from presentation.contracts.http.routers import AbstractHttpSettingsRouter
from presentation.contracts.http.mappers import AbstractSettingsRouterMapper
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import (
    SettingsSchema,
    SettingsUpdateSchema
)
from presentation.shared import CookieConstants


class HttpSettingsRouter(AbstractHttpSettingsRouter, HttpBaseRouter):
    """
    Handles HTTP routes for settings operations.
    """
    router: APIRouter
    settings_service: AbstractSettingsService
    settings_mapper: AbstractSettingsRouterMapper

    def __init__(
        self,
        router: APIRouter,
        settings_service: AbstractSettingsService,
        settings_mapper: AbstractSettingsRouterMapper,
        auth_service: AbstractAuthService
    ):
        HttpBaseRouter.__init__(self, auth_service)

        self.router = router
        self.settings_service = settings_service
        self.settings_mapper = settings_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/settings",
            tags=["Settings"],
            dependencies=[
                Depends(self.session_required)
            ]
        )

        router.add_api_route(
            path="/me",
            endpoint=self.update_me,
            methods=["PATCH"],
            operation_id="settings_update_me",
            response_model=SettingsSchema
        )

        router.add_api_route(
            path="/cache",
            endpoint=self.clear_cache,
            methods=["DELETE"],
            operation_id="settings_clear_cache",
            dependencies=[
                Depends(self.one_of_permissions_required(
                    permissions=[
                        PermissionEnum.SETTINGS_CACHE_CLEAR
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/containers",
            endpoint=self.clear_containers,
            methods=["DELETE"],
            operation_id="settings_clear_containers",
            dependencies=[
                Depends(self.one_of_permissions_required(
                    permissions=[
                        PermissionEnum.SETTINGS_CONTAINERS_CLEAR
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def update_me(
        self,
        request: Request,
        schema: SettingsUpdateSchema = Body(...)
    ) -> Response:
        """
        Updates settings for the currently authenticated user.

        Parameters:
        - request: Request object.
        - schema: SettingsUpdateSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.settings_mapper.update_schema_to_dto(
            schema=schema
        )

        response_dto = await self.settings_service.update_one(
            user_id=request.state.user.id,
            current_user=request.state.user,
            dto=request_dto
        )

        response_schema = self.settings_mapper.dto_to_schema(
            dto=response_dto
        )

        response = JSONResponse(
            content=response_schema.model_dump(mode="json")
        )

        response.set_cookie(
            key=CookieConstants.LANGUAGE_KEY,
            value=response_dto.language,
            httponly=False,
            secure=True,
            samesite="strict",
            path="/",
            max_age=CookieConstants.EXPIRATION_SECONDS
        )

        return response

    async def clear_cache(self) -> Response:
        """
        Clears application cached data.

        Parameters:
        - None.

        Returns:
        - Response: Response object.
        """
        await self.settings_service.clear_cache()

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def clear_containers(self) -> Response:
        """
        Clears unused containers data.

        Parameters:
        - None.

        Returns:
        - Response: Response object.
        """
        await self.settings_service.clear_containers()

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
