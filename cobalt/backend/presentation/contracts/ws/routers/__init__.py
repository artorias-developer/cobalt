#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .base import AbstractWsRouter
from .events import AbstractWsEventsRouter

__all__ = [
    "AbstractWsRouter",
    "AbstractWsEventsRouter"
]