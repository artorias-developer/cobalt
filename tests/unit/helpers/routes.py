#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
Table-driven access/dispatch checks for HTTP routers.

A test class inherits `RouteContract`, declares `ROUTES` and provides `client` and `service`
fixtures. `pytest_generate_tests` in routers/conftest.py parametrizes every test with each route.
For each route it checks that:
- a request without a session returns 401;
- a user with every permission except the allowed ones gets 403;
- a user with only one of the allowed permissions passes, and the service method is awaited
  with the expected arguments.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from fastapi import status

from domain.enums import PermissionEnum


@dataclass(frozen=True)
class Route:
    method: str
    path: str
    service_method: str
    permissions: List[PermissionEnum]
    call_kwargs: Dict[str, Any] = field(default_factory=dict)
    json: Any = None
    params: Optional[Dict[str, Any]] = None
    return_value: Any = None
    status: int = status.HTTP_200_OK

    @property
    def id(self) -> str:
        return f"{self.method} {self.path}"


def send(client, route: Route):
    return client.request(route.method, route.path, json=route.json, params=route.params)


def all_permissions_except(permissions: List[PermissionEnum]) -> List[PermissionEnum]:
    return [permission for permission in PermissionEnum if permission not in permissions]


class RouteContract:
    ROUTES: List[Route] = []

    def test_requires_session(self, client, service, route: Route):
        response = send(client, route)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        getattr(service, route.service_method).assert_not_awaited()

    def test_forbidden_without_permission(self, client, login_as, service, route: Route):
        login_as(client, permissions=all_permissions_except(route.permissions))

        response = send(client, route)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"message": "Not enough permissions"}
        getattr(service, route.service_method).assert_not_awaited()

    def test_allowed_with_any_listed_permission(self, client, login_as, service, route: Route):
        service_method = getattr(service, route.service_method)
        service_method.return_value = route.return_value

        for permission in route.permissions:
            service_method.reset_mock()
            login_as(client, permissions=[permission])

            response = send(client, route)

            assert response.status_code == route.status, (permission, response.text)
            service_method.assert_awaited_once_with(**route.call_kwargs)
