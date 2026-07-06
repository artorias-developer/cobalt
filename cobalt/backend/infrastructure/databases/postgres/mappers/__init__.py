#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .attributes import AttributesRepositoryMapper
from .games import GamesRepositoryMapper
from .loaders import LoadersRepositoryMapper
from .roles import RolesRepositoryMapper
from .servers import ServersRepositoryMapper
from .settings import SettingsRepositoryMapper
from .users import UsersRepositoryMapper

__all__ = [
    "AttributesRepositoryMapper",
    "GamesRepositoryMapper",
    "LoadersRepositoryMapper",
    "RolesRepositoryMapper",
    "ServersRepositoryMapper",
    "SettingsRepositoryMapper",
    "UsersRepositoryMapper"
]
