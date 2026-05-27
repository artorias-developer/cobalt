#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .attributes import AbstractAttributesRepositoryMapper
from .games import AbstractGamesRepositoryMapper
from .loaders import AbstractLoadersRepositoryMapper
from .roles import AbstractRolesRepositoryMapper
from .servers import AbstractServersRepositoryMapper
from .settings import AbstractSettingsRepositoryMapper
from .users import AbstractUsersRepositoryMapper

__all__ = [
    "AbstractAttributesRepositoryMapper",
    "AbstractGamesRepositoryMapper",
    "AbstractLoadersRepositoryMapper",
    "AbstractRolesRepositoryMapper",
    "AbstractServersRepositoryMapper",
    "AbstractSettingsRepositoryMapper",
    "AbstractUsersRepositoryMapper"
]
