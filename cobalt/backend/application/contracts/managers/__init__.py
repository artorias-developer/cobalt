#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .archives import AbstractArchivesManager
from .connections import AbstractConnectionsManager
from .events import AbstractEventsManager
from .i18n import AbstractI18nManager

__all__ = [
    "AbstractArchivesManager",
    "AbstractConnectionsManager",
    "AbstractEventsManager",
    "AbstractI18nManager"
]
