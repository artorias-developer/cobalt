#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from enum import StrEnum


class ServerSortFieldEnum(StrEnum):
    ID = "id"
    NAME = "name"
    GAME_ID = "game_id"
    LOADER_ID = "loader_id"
    VERSION = "version"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"

class ServerStateEnum(StrEnum):
    """
    Server state enum.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    UPGRADING = "upgrading"
    CREATED = "created"
    FAILED = "failed"
    UPGRADE_FAILED = "upgrade_failed"