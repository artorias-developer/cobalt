#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Request, Response, status, Depends, Body

from domain.enums import PermissionsEnum
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import (
    AbstractUsersService,
    AbstractAuthService
)
from presentation.contracts.http.routers import AbstractHttpUsersRouter
from presentation.contracts.http.mappers import AbstractUsersRouterMapper
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import (
    UserSchema,
    UserMeSchema,
    UsersGetPageSchema,
    UsersPageSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UsersDeleteSchema
)


class HttpUsersRouter(AbstractHttpUsersRouter, HttpBaseRouter):
    """
    Handles HTTP routes for users operations.
    """
    router: APIRouter
    users_service: AbstractUsersService
    users_mapper: AbstractUsersRouterMapper

    def __init__(
        self,
        router: APIRouter,
        users_service: AbstractUsersService,
        users_mapper: AbstractUsersRouterMapper,
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        HttpBaseRouter.__init__(self, auth_service, i18n_manager)

        self.router = router
        self.users_service = users_service
        self.users_mapper = users_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/users",
            tags=["Users"],
            dependencies=[
                Depends(self.http_session_required)
            ]
        )

        router.add_api_route(
            path="/batch",
            endpoint=self.delete_many,
            methods=["DELETE"],
            operation_id="users_delete_many",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.USERS_DELETE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.get_page,
            methods=["GET"],
            operation_id="users_get_page",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.USERS_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/me",
            endpoint=self.get_me,
            methods=["GET"],
            operation_id="users_get_me"
        )

        router.add_api_route(
            path="/{user_id}",
            endpoint=self.get_one,
            methods=["GET"],
            operation_id="users_get_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.USERS_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.create_one,
            methods=["POST"],
            operation_id="users_create_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.USERS_CREATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{user_id}",
            endpoint=self.update_one,
            methods=["PATCH"],
            operation_id="users_update_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.USERS_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{user_id}",
            endpoint=self.delete_one,
            methods=["DELETE"],
            operation_id="users_delete_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.USERS_DELETE
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def get_page(
        self,
        schema: UsersGetPageSchema = Depends()
    ) -> UsersPageSchema:
        """
        Gets a paginated list of users.

        Parameters:
        - schema: UsersGetPageSchema object.

        Returns:
        - UsersPageSchema: UsersPageSchema object.
        """
        request_dto = self.users_mapper.get_page_schema_to_dto(
            schema=schema
        )

        response_dto = await self.users_service.get_page(
            dto=request_dto
        )

        return self.users_mapper.page_dto_to_schema(
            dto=response_dto
        )

    async def get_me(
        self,
        request: Request
    ) -> UserMeSchema:
        """
        Gets the currently authenticated user.

        Parameters:
        - request: Request object.

        Returns:
        - UserMeSchema: UserMeSchema object.
        """
        return self.users_mapper.dto_to_me_schema(
            dto=request.state.user
        )

    async def get_one(
        self,
        user_id: int
    ) -> UserSchema:
        """
        Gets an existing user.

        Parameters:
        - user_id: User ID.

        Returns:
        - UserSchema: UserSchema object.
        """
        response_dto = await self.users_service.get_one_by_id(
            user_id=user_id
        )

        return self.users_mapper.dto_to_schema(
            dto=response_dto
        )

    async def create_one(
        self,
        schema: UserCreateSchema = Body(...)
    ) -> UserSchema:
        """
        Creates a new user.

        Parameters:
        - schema: UserCreateSchema object.

        Returns:
        - UserSchema: UserSchema object.
        """
        request_dto = self.users_mapper.create_schema_to_dto(
            schema=schema
        )

        response_dto = await self.users_service.create_one(
            dto=request_dto
        )

        return self.users_mapper.dto_to_schema(
            dto=response_dto
        )

    async def update_one(
        self,
        user_id: int,
        schema: UserUpdateSchema = Body(...)
    ) -> UserSchema:
        """
        Updates an existing user.

        Parameters:
        - user_id: User ID.
        - schema: UserUpdateSchema object.

        Returns:
        - UserSchema: UserSchema object.
        """
        request_dto = self.users_mapper.update_schema_to_dto(
            schema=schema
        )

        response_dto = await self.users_service.update_one(
            user_id=user_id,
            dto=request_dto
        )

        return self.users_mapper.dto_to_schema(
            dto=response_dto
        )

    async def delete_one(
        self,
        user_id: int
    ) -> Response:
        """
        Deletes an existing user.

        Parameters:
        - user_id: User ID.

        Returns:
        - Response: Response object.
        """
        await self.users_service.delete_one(
            user_id=user_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def delete_many(
        self,
        schema: UsersDeleteSchema = Body(...)
    ) -> Response:
        """
        Deletes multiple existing users.

        Parameters:
        - schema: UsersDeleteSchema object.

        Returns:
        - Response: Response object.
        """
        await self.users_service.delete_many(
            user_ids=schema.root
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
