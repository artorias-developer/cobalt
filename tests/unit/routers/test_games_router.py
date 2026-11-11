#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import PermissionEnum, GameSortFieldEnum, SortDirectionEnum
from domain.exceptions import NotFoundError
from application.dtos import GamesPageDto, GamesGetPageDto
from presentation.http.fastapi.v1.mappers import GamesRouterMapper, LoadersRouterMapper
from presentation.http.fastapi.v1.routers import HttpGamesRouter

from helpers.app import build_test_client
from helpers.factories import make_game_dto
from helpers.routes import Route, RouteContract


URL = "/api/v1/games"

PAGE = GamesPageDto(games=[make_game_dto()], total=1, page=1, pages=1)


@pytest.fixture
def service(games_service_mock):
    return games_service_mock


@pytest.fixture
def client(games_service_mock, auth_service_mock, i18n_manager, logger):
    with build_test_client(
        router_factories=[
            lambda api: HttpGamesRouter(
                router=api,
                games_service=games_service_mock,
                games_mapper=GamesRouterMapper(loaders_mapper=LoadersRouterMapper()),
                auth_service=auth_service_mock
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


class TestGamesRoutes(RouteContract):
    ROUTES = [
        Route(
            "GET", f"{URL}/", "get_page",
            permissions=[PermissionEnum.GAMES_VIEW, PermissionEnum.SERVERS_CREATE],
            call_kwargs={"dto": GamesGetPageDto(page=1)},
            return_value=PAGE
        ),
        Route(
            "GET", f"{URL}/3", "get_one_by_id",
            permissions=[PermissionEnum.SERVERS_CREATE],
            call_kwargs={"game_id": 3},
            return_value=make_game_dto(game_id=3)
        )
    ]


class TestGetPage:
    def test_maps_query_and_response(self, client, login_as, games_service_mock):
        login_as(client)
        games_service_mock.get_page.return_value = PAGE

        response = client.get(
            f"{URL}/",
            params={"page": 2, "search": "mine", "sort_field": "name", "sort_direction": "asc", "limit": 20}
        )

        assert response.status_code == status.HTTP_200_OK
        game = response.json()["games"][0]
        assert game["name"] == "minecraft"
        assert game["loaders"][0]["name"] == "vanilla"
        games_service_mock.get_page.assert_awaited_once_with(
            dto=GamesGetPageDto(
                page=2,
                search="mine",
                sort_field=GameSortFieldEnum.NAME,
                sort_direction=SortDirectionEnum.ASC,
                limit=20
            )
        )

    def test_not_found(self, client, login_as, games_service_mock):
        login_as(client)
        games_service_mock.get_page.side_effect = NotFoundError("Games not found")

        response = client.get(f"{URL}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "Games not found"}


class TestGetOne:
    def test_non_integer_id_returns_422(self, client, login_as, games_service_mock):
        login_as(client)

        response = client.get(f"{URL}/minecraft")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        games_service_mock.get_one_by_id.assert_not_awaited()
