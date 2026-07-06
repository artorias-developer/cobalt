#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .attributes import AttributesServiceMapper
from .games import GamesServiceMapper
from .loaders import LoadersServiceMapper
from .logs import LogsServiceMapper
from .metrics import MetricsServiceMapper
from .roles import RolesServiceMapper
from .servers import ServersServiceMapper
from .settings import SettingsServiceMapper
from .users import UsersServiceMapper

__all__ = [
    "AttributesServiceMapper",
    "GamesServiceMapper",
    "LoadersServiceMapper",
    "LogsServiceMapper",
    "MetricsServiceMapper",
    "RolesServiceMapper",
    "ServersServiceMapper",
    "SettingsServiceMapper",
    "UsersServiceMapper"
]
