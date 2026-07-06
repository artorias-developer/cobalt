#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .base import HttpBaseRouter
from .attributes import HttpAttributesRouter
from .auth import HttpAuthRouter
from .files import HttpFilesRouter
from .games import HttpGamesRouter
from .logs import HttpLogsRouter
from .metrics import HttpMetricsRouter
from .roles import HttpRolesRouter
from .servers import HttpServersRouter
from .settings import HttpSettingsRouter
from .users import HttpUsersRouter

__all__ = [
    "HttpBaseRouter",
    "HttpAttributesRouter",
    "HttpAuthRouter",
    "HttpFilesRouter",
    "HttpGamesRouter",
    "HttpLogsRouter",
    "HttpMetricsRouter",
    "HttpRolesRouter",
    "HttpServersRouter",
    "HttpSettingsRouter",
    "HttpUsersRouter"
]
