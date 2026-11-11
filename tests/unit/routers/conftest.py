#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Callable, List, Optional

import pytest

from domain.enums import PermissionEnum
from application.dtos import UserDto
from presentation.shared import CookieConstants

from helpers.factories import make_role_dto, make_user_dto


SESSION_ID = "test-session"


def pytest_generate_tests(metafunc):
    # Parametrize RouteContract tests with the ROUTES of the concrete test class.
    routes = getattr(metafunc.cls, "ROUTES", None)

    if routes and "route" in metafunc.fixturenames:
        metafunc.parametrize("route", routes, ids=[route.id for route in routes])


@pytest.fixture
def login_as(auth_service_mock) -> Callable[..., UserDto]:
    """
    Makes the mocked auth middleware resolve the test session cookie to a user
    with the given permissions. Call with `permissions=None` to grant all of them.
    """
    def _login_as(
        client,
        permissions: Optional[List[PermissionEnum]] = None,
        user_id: int = 1
    ) -> UserDto:
        user = make_user_dto(
            user_id=user_id,
            role=make_role_dto(permissions=permissions)
        )
        auth_service_mock.get_session_user.return_value = user
        client.cookies.set(CookieConstants.SESSION_KEY, SESSION_ID)
        return user

    return _login_as
