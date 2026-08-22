#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from enum import StrEnum


class GameSortFieldEnum(StrEnum):
    ID = "id"
    NAME = "name"
    LOADER_ID = "loader_id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"