#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .attributes import AttributesRouterMapper
from .auth import AuthRouterMapper
from .files import FilesRouterMapper
from .games import GamesRouterMapper
from .loaders import LoadersRouterMapper
from .logs import LogsRouterMapper
from .metrics import MetricsRouterMapper
from .roles import RolesRouterMapper
from .servers import ServersRouterMapper
from .settings import SettingsRouterMapper
from .users import UsersRouterMapper

__all__ = [
    "AttributesRouterMapper",
    "AuthRouterMapper",
    "FilesRouterMapper",
    "GamesRouterMapper",
    "LoadersRouterMapper",
    "LogsRouterMapper",
    "MetricsRouterMapper",
    "RolesRouterMapper",
    "ServersRouterMapper",
    "SettingsRouterMapper",
    "UsersRouterMapper"
]
