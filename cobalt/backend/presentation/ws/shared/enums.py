#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from enum import IntEnum


class WebSocketStatusCodesEnum(IntEnum):
    """
    WebSockets error codes enum.
    """
    WS_1011_INTERNAL_SERVER_ERROR = 1011
    WS_4400_BAD_REQUEST = 4400
    WS_4401_UNAUTHORIZED = 4401
    WS_4403_FORBIDDEN = 4403
    WS_4404_NOT_FOUND = 4404
    WS_4409_CONFLICT = 4409
