#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .attributes import AbstractAttributesRepository
from .games import AbstractGamesRepository
from .loaders import AbstractLoadersRepository
from .roles import AbstractRolesRepository
from .servers import AbstractServersRepository
from .settings import AbstractSettingsRepository
from .users import AbstractUsersRepository

__all__ = [
    "AbstractAttributesRepository",
    "AbstractGamesRepository",
    "AbstractLoadersRepository",
    "AbstractRolesRepository",
    "AbstractUsersRepository",
    "AbstractServersRepository",
    "AbstractSettingsRepository",
    "AbstractUsersRepository"
]
