#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Request, Response, Body, status, Depends

from application.contracts.services import AbstractAuthService
from presentation.contracts.http.mappers import AbstractAuthRouterMapper
from presentation.contracts.http.routers import AbstractHttpAuthRouter
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import (
    AuthLoginSchema,
    AuthChangeCredentialsSchema
)
from presentation.shared import CookieConstants


class HttpAuthRouter(AbstractHttpAuthRouter, HttpBaseRouter):
    """
    Handles HTTP routes for authentication.
    """
    router: APIRouter
    auth_service: AbstractAuthService
    auth_mapper: AbstractAuthRouterMapper

    def __init__(
        self,
        router: APIRouter,
        auth_service: AbstractAuthService,
        auth_mapper: AbstractAuthRouterMapper
    ):
        HttpBaseRouter.__init__(self, auth_service)

        self.router = router
        self.auth_service = auth_service
        self.auth_mapper = auth_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/auth",
            tags=["Auth"]
        )

        router.add_api_route(
            path="/login",
            endpoint=self.login,
            methods=["POST"],
            operation_id="auth_login"
        )

        router.add_api_route(
            path="/logout",
            endpoint=self.logout,
            methods=["POST"],
            operation_id="auth_logout"
        )

        router.add_api_route(
            path="/credentials",
            endpoint=self.change_credentials,
            methods=["PATCH"],
            operation_id="auth_change_credentials",
            dependencies=[
                Depends(self.http_session_required)
            ]
        )

        self.router.include_router(router)

    async def login(
        self,
        request: Request,
        schema: AuthLoginSchema = Body(...)
    ) -> Response:
        """
        Authenticates a user and creates a session.

        Parameters:
        - schema: AuthLoginSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.auth_mapper.login_schema_to_dto(
            schema=schema
        )

        response_dto = await self.auth_service.login(
            old_session_id=request.cookies.get(CookieConstants.SESSION_KEY),
            dto=request_dto
        )

        response = Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

        response.set_cookie(
            key=CookieConstants.SESSION_KEY,
            value=response_dto.session_id,
            httponly=True,
            secure=True,
            samesite="strict",
            path="/",
            max_age=CookieConstants.EXPIRATION_SECONDS
        )

        return response

    async def logout(
        self,
        request: Request
    ) -> Response:
        """
        Deletes the user's session.

        Parameters:
        - None.

        Returns:
        - Response: Response object.
        """
        session_id = request.cookies.get(CookieConstants.SESSION_KEY)

        if session_id:
            await self.auth_service.logout(
                session_id=session_id
            )

        response = Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

        response.delete_cookie(
            key=CookieConstants.SESSION_KEY,
            path="/"
        )

        return response

    async def change_credentials(
        self,
        request: Request,
        schema: AuthChangeCredentialsSchema = Body(...)
    ) -> Response:
        """
        Changes login and/or password for the currently authenticated user.

        Parameters:
        - request: Request object.
        - schema: AuthChangeCredentialsSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.auth_mapper.change_credentials_schema_to_dto(
            schema=schema
        )

        await self.auth_service.change_credentials(
            user_id=request.state.user.id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
