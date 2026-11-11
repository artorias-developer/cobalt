#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import LanguageEnum
from domain.exceptions import AuthenticationError, ConflictError
from application.dtos import (
    AuthLoginDto,
    AuthSessionDto,
    AuthUpdateCredentialsDto
)
from presentation.http.fastapi.v1.mappers import AuthRouterMapper
from presentation.http.fastapi.v1.routers import HttpAuthRouter
from presentation.shared import CookieConstants

from helpers.app import build_test_client
from helpers.factories import make_user_dto


URL = "/api/v1/auth"


@pytest.fixture
def client(auth_service_mock, i18n_manager, logger):
    with build_test_client(
        router_factories=[
            lambda api: HttpAuthRouter(
                router=api,
                auth_service=auth_service_mock,
                auth_mapper=AuthRouterMapper()
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


def _set_cookie_headers(response) -> dict:
    """
    Returns a {cookie_name: raw Set-Cookie header} mapping.
    """
    return {
        header.split("=", 1)[0]: header
        for header in response.headers.get_list("set-cookie")
    }


class TestLogin:
    def test_sets_secure_session_and_language_cookies(self, client, auth_service_mock):
        auth_service_mock.login.return_value = AuthSessionDto(session_id="new-session")
        auth_service_mock.get_session_user.return_value = make_user_dto(language=LanguageEnum.UK)

        response = client.post(f"{URL}/login", json={"login": "john_doe", "password": "Secret123"})

        assert response.status_code == status.HTTP_204_NO_CONTENT
        cookies = _set_cookie_headers(response)

        session_cookie = cookies[CookieConstants.SESSION_KEY].lower()
        assert "session_id=new-session" in session_cookie
        assert "httponly" in session_cookie
        assert "secure" in session_cookie
        assert "samesite=strict" in session_cookie

        language_cookie = cookies[CookieConstants.LANGUAGE_KEY].lower()
        assert "language=uk" in language_cookie
        assert "httponly" not in language_cookie

    def test_passes_previous_session_to_service(self, client, auth_service_mock):
        auth_service_mock.login.return_value = AuthSessionDto(session_id="new-session")
        client.cookies.set(CookieConstants.SESSION_KEY, "old-session")

        client.post(f"{URL}/login", json={"login": "john_doe", "password": "Secret123"})

        auth_service_mock.login.assert_awaited_once_with(
            old_session_id="old-session",
            dto=AuthLoginDto(login="john_doe", password="Secret123")
        )

    def test_invalid_credentials_return_401_without_cookie(self, client, auth_service_mock):
        auth_service_mock.login.side_effect = AuthenticationError("Invalid login or password")

        response = client.post(f"{URL}/login", json={"login": "john_doe", "password": "wrong"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"message": "Invalid login or password"}
        assert CookieConstants.SESSION_KEY not in _set_cookie_headers(response)

    def test_missing_password_returns_422(self, client, auth_service_mock):
        response = client.post(f"{URL}/login", json={"login": "john_doe"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Password is required"}
        auth_service_mock.login.assert_not_awaited()


class TestLogout:
    def test_deletes_session_and_clears_cookie(self, client, auth_service_mock):
        client.cookies.set(CookieConstants.SESSION_KEY, "abc")

        response = client.post(f"{URL}/logout")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        auth_service_mock.logout.assert_awaited_once_with(session_id="abc")
        cleared = _set_cookie_headers(response)[CookieConstants.SESSION_KEY].lower()
        assert "max-age=0" in cleared

    def test_without_cookie_does_not_call_service(self, client, auth_service_mock):
        response = client.post(f"{URL}/logout")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        auth_service_mock.logout.assert_not_awaited()


class TestUpdateCredentials:
    def test_requires_session(self, client, auth_service_mock):
        response = client.patch(f"{URL}/credentials", json={"login": "new_login"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        auth_service_mock.update_credentials.assert_not_awaited()

    def test_updates_credentials_of_current_user(self, client, login_as, auth_service_mock):
        login_as(client, user_id=12)

        response = client.patch(
            f"{URL}/credentials",
            json={"old_password": "OldPass1", "new_password": "NewPass1"}
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        auth_service_mock.update_credentials.assert_awaited_once_with(
            user_id=12,
            dto=AuthUpdateCredentialsDto(login=None, old_password="OldPass1", new_password="NewPass1")
        )

    def test_wrong_old_password_returns_409(self, client, login_as, auth_service_mock):
        login_as(client)
        auth_service_mock.update_credentials.side_effect = ConflictError("Invalid current password")

        response = client.patch(
            f"{URL}/credentials",
            json={"old_password": "nope", "new_password": "NewPass1"}
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {"message": "Invalid current password"}
