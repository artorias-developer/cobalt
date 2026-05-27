#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC

from presentation.contracts.ws.routers import AbstractWsRouter


class AbstractWsEventsRouter(AbstractWsRouter, ABC):
    """
    Abstract WebSockets router for events-related operations.
    """
    ...