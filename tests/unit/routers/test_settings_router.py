#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import PermissionEnum, LanguageEnum, ThemeEnum
from domain.exceptions import UnexpectedError
from application.dtos import SettingsUpdateDto
from presentation.http.fastapi.v1.mappers import SettingsRouterMapper
from presentation.http.fastapi.v1.routers import HttpSettingsRouter
from presentation.shared import CookieConstants

from helpers.app import build_test_client
from helpers.factories import make_settings_dto
from helpers.routes import Route, RouteContract


URL = "/api/v1/settings"


@pytest.fixture
def service(settings_service_mock):
    return settings_service_mock


@pytest.fixture
def client(settings_service_mock, auth_service_mock, i18n_manager, logger):
    with build_test_client(
        router_factories=[
            lambda api: HttpSettingsRouter(
                router=api,
                settings_service=settings_service_mock,
                settings_mapper=SettingsRouterMapper(),
                auth_service=auth_service_mock
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


class TestSettingsRoutes(RouteContract):
    ROUTES = [
        Route(
            "DELETE", f"{URL}/cache", "clear_cache",
            permissions=[PermissionEnum.SETTINGS_CACHE_CLEAR],
            status=status.HTTP_204_NO_CONTENT
        ),
        Route(
            "DELETE", f"{URL}/containers", "clear_containers",
            permissions=[PermissionEnum.SETTINGS_CONTAINERS_CLEAR],
            status=status.HTTP_204_NO_CONTENT
        )
    ]


class TestUpdateMe:
    def test_requires_session(self, client, settings_service_mock):
        response = client.patch(f"{URL}/me", json={"theme": "cobalt_light"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        settings_service_mock.update_one.assert_not_awaited()

    def test_works_without_permissions_and_targets_current_user(self, client, login_as, settings_service_mock):
        login_as(client, permissions=[], user_id=7)
        settings_service_mock.update_one.return_value = make_settings_dto(user_id=7)

        response = client.patch(f"{URL}/me", json={"theme": "cobalt_light"})

        assert response.status_code == status.HTTP_200_OK
        settings_service_mock.update_one.assert_awaited_once_with(
            user_id=7,
            dto=SettingsUpdateDto(language=None, theme=ThemeEnum.COBALT_LIGHT, timezone=None)
        )

    def test_sets_language_cookie_from_saved_settings(self, client, login_as, settings_service_mock):
        login_as(client)
        settings_service_mock.update_one.return_value = make_settings_dto(language=LanguageEnum.RU)

        response = client.patch(f"{URL}/me", json={"language": "ru"})

        assert response.json()["language"] == "ru"
        language_cookie = next(
            header for header in response.headers.get_list("set-cookie")
            if header.startswith(f"{CookieConstants.LANGUAGE_KEY}=")
        ).lower()
        assert "language=ru" in language_cookie
        assert "secure" in language_cookie
        assert "httponly" not in language_cookie

    def test_unknown_language_returns_422(self, client, login_as, settings_service_mock):
        login_as(client)

        response = client.patch(f"{URL}/me", json={"language": "klingon"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json()["message"].startswith("Language must be one of the allowed values")
        settings_service_mock.update_one.assert_not_awaited()


class TestClearContainers:
    def test_service_failure_returns_500(self, client, login_as, settings_service_mock):
        login_as(client)
        settings_service_mock.clear_containers.side_effect = UnexpectedError("Docker is unavailable")

        response = client.delete(f"{URL}/containers")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"message": "Docker is unavailable"}
