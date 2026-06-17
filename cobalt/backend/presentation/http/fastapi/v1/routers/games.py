#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, Depends

from domain.enums import PermissionsEnum
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import (
    AbstractGamesService,
    AbstractAuthService
)
from presentation.contracts.http.routers import AbstractHttpGamesRouter
from presentation.contracts.http.mappers import AbstractGamesRouterMapper
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import (
    GameSchema,
    GamesGetPageSchema,
    GamesPageSchema
)


class HttpGamesRouter(AbstractHttpGamesRouter, HttpBaseRouter):
    """
    Handles HTTP routes for games operations.
    """
    router: APIRouter
    games_service: AbstractGamesService
    games_mapper: AbstractGamesRouterMapper

    def __init__(
        self,
        router: APIRouter,
        games_service: AbstractGamesService,
        games_mapper: AbstractGamesRouterMapper,
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        HttpBaseRouter.__init__(self, auth_service, i18n_manager)

        self.router = router
        self.games_service = games_service
        self.games_mapper = games_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/games",
            tags=["Games"],
            dependencies=[
                Depends(self.http_session_required)
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.get_page,
            methods=["GET"],
            operation_id="games_get_page",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.GAMES_VIEW,
                        PermissionsEnum.SERVERS_CREATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/{game_id}",
            endpoint=self.get_one,
            methods=["GET"],
            operation_id="games_get_one",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVERS_CREATE
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def get_page(
        self,
        schema: GamesGetPageSchema = Depends()
    ) -> GamesPageSchema:
        """
        Gets a paginated list of games.

        Parameters:
        - schema: GamesGetPageSchema object.

        Returns:
        - GamesPageSchema: GamesPageSchema object.
        """
        request_dto = self.games_mapper.get_page_schema_to_dto(
            schema=schema
        )

        response_dto = await self.games_service.get_page(
            dto=request_dto
        )

        return self.games_mapper.page_dto_to_schema(
            dto=response_dto
        )

    async def get_one(
        self,
        game_id: int
    ) -> GameSchema:
        """
        Gets an existing game by ID.

        Parameters:
        - game_id: Game ID.

        Returns:
        - GameSchema: GameSchema object.
        """
        response_dto = await self.games_service.get_one_by_id(
            game_id=game_id
        )

        return self.games_mapper.dto_to_schema(
            dto=response_dto
        )