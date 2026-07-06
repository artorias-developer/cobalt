#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .base import AbstractHttpRouter
from .attributes import AbstractHttpAttributesRouter
from .auth import AbstractHttpAuthRouter
from .files import AbstractHttpFilesRouter
from .games import AbstractHttpGamesRouter
from .logs import AbstractHttpLogsRouter
from .metrics import AbstractHttpMetricsRouter
from .roles import AbstractHttpRolesRouter
from .servers import AbstractHttpServersRouter
from .settings import AbstractHttpSettingsRouter
from .users import AbstractHttpUsersRouter

__all__ = [
    "AbstractHttpRouter",
    "AbstractHttpAttributesRouter",
    "AbstractHttpAuthRouter",
    "AbstractHttpFilesRouter",
    "AbstractHttpGamesRouter",
    "AbstractHttpLogsRouter",
    "AbstractHttpMetricsRouter",
    "AbstractHttpRolesRouter",
    "AbstractHttpServersRouter",
    "AbstractHttpSettingsRouter",
    "AbstractHttpUsersRouter"
]