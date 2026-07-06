#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Request, Response, Depends, Body, status

from domain.enums import PermissionsEnum
from application.contracts.managers import AbstractI18nManager
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
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        HttpBaseRouter.__init__(self, auth_service, i18n_manager)

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
                Depends(self.http_session_required)
            ]
        )

        router.add_api_route(
            path="/me",
            endpoint=self.update_me,
            methods=["PATCH"],
            operation_id="settings_update_me"
        )

        router.add_api_route(
            path="/cache",
            endpoint=self.clear_cache,
            methods=["DELETE"],
            operation_id="settings_clear_cache",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SETTINGS_CACHE_CLEAR
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
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SETTINGS_CONTAINERS_CLEAR
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def update_me(
        self,
        request: Request,
        schema: SettingsUpdateSchema = Body(...)
    ) -> SettingsSchema:
        """
        Updates settings for the currently authenticated user.

        Parameters:
        - request: Request object.
        - schema: SettingsUpdateSchema object.

        Returns:
        - SettingsSchema: SettingsSchema object.
        """
        request_dto = self.settings_mapper.update_schema_to_dto(
            schema=schema
        )

        response_dto = await self.settings_service.update_one(
            user_id=request.state.user.id,
            current_user=request.state.user,
            dto=request_dto
        )

        return self.settings_mapper.dto_to_schema(
            dto=response_dto
        )

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
