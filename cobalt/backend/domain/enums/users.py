#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from enum import StrEnum


class UserSortFieldEnum(StrEnum):
    ID = "id"
    LOGIN = "login"
    ROLE_ID = "role_id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"