#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI, Request, status
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient

from domain.exceptions import (
    BaseError,
    UnexpectedError,
    ValidationError,
    AuthenticationError,
    PermissionsError,
    NotFoundError,
    ConflictError
)
from presentation.http.fastapi.v1.middlewares import (
    HttpErrorsMiddleware,
    HttpAuthMiddleware
)
from presentation.shared import CookieConstants

from helpers.factories import make_user_dto


class UnmappedError(BaseError):
    ...


@pytest.fixture
def errors_middleware(i18n_manager, logger) -> HttpErrorsMiddleware:
    return HttpErrorsMiddleware(app=AsyncMock(), i18n_manager=i18n_manager, logger=logger)


class TestHttpErrorsMapping:
    @pytest.mark.parametrize(
        ("error", "expected_status"),
        [
            (UnexpectedError("x"), status.HTTP_500_INTERNAL_SERVER_ERROR),
            (ValidationError("x"), status.HTTP_400_BAD_REQUEST),
            (AuthenticationError("x"), status.HTTP_401_UNAUTHORIZED),
            (PermissionsError("x"), status.HTTP_403_FORBIDDEN),
            (NotFoundError("x"), status.HTTP_404_NOT_FOUND),
            (ConflictError("x"), status.HTTP_409_CONFLICT)
        ]
    )
    def test_domain_errors_map_to_http_status(self, errors_middleware, error, expected_status):
        code, _ = errors_middleware.get_http_error(error)

        assert code == expected_status

    def test_message_is_translated_then_formatted(self, errors_middleware, i18n_manager):
        i18n_manager.gettext.side_effect = lambda message: f"[uk] {message}"

        _, message = errors_middleware.get_http_error(NotFoundError("Role {role_id} not found", role_id=5))

        i18n_manager.gettext.assert_called_once_with("Role {role_id} not found")
        assert message == "[uk] Role 5 not found"

    def test_unmapped_base_error_falls_back_to_500_with_warning(self, errors_middleware, logger):
        code, message = errors_middleware.get_http_error(UnmappedError("boom"))

        assert code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert message == "boom"
        logger.warning.assert_called_once()

    def test_unknown_exception_hides_details(self, errors_middleware, logger):
        code, message = errors_middleware.get_http_error(KeyError("secret internals"))

        assert code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert message == "Internal server error"
        logger.exception.assert_called_once()


class TestHttpErrorsMiddlewareStreaming:
    def test_error_after_response_started_is_reraised(self, i18n_manager, logger):
        app = FastAPI()

        async def broken_stream():
            yield b"partial"
            raise RuntimeError("mid-stream")

        @app.get("/stream")
        async def stream():
            return StreamingResponse(broken_stream())

        app.add_middleware(HttpErrorsMiddleware, i18n_manager=i18n_manager, logger=logger)

        with TestClient(app) as client, pytest.raises(RuntimeError, match="mid-stream"):
            client.get("/stream")

        logger.exception.assert_called_once()


class TestHttpAuthMiddleware:
    @pytest.fixture
    def client(self, auth_service_mock):
        app = FastAPI()

        @app.get("/whoami")
        async def whoami(request: Request):
            user = getattr(request.state, "user", None)
            return {"user_id": user.id if user else None}

        app.add_middleware(HttpAuthMiddleware, auth_service=auth_service_mock)

        with TestClient(app) as test_client:
            yield test_client

    def test_without_cookie_skips_lookup(self, client, auth_service_mock):
        assert client.get("/whoami").json() == {"user_id": None}

        auth_service_mock.get_session_user.assert_not_awaited()

    def test_valid_cookie_sets_request_user(self, client, auth_service_mock):
        auth_service_mock.get_session_user.return_value = make_user_dto(user_id=42)
        client.cookies.set(CookieConstants.SESSION_KEY, "abc")

        assert client.get("/whoami").json() == {"user_id": 42}

        auth_service_mock.get_session_user.assert_awaited_once_with(session_id="abc")

    def test_service_failure_is_treated_as_anonymous(self, client, auth_service_mock):
        auth_service_mock.get_session_user.side_effect = ConnectionError("redis down")
        client.cookies.set(CookieConstants.SESSION_KEY, "abc")

        response = client.get("/whoami")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"user_id": None}
