#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from enum import StrEnum


class RoleEventEnum(StrEnum):
    """
    WebSocket roles events enum.
    """
    ROLE_UPDATE = "role_update"
    USER_ROLE_UPDATE = "user_role_update"