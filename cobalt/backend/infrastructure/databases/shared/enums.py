#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from enum import StrEnum


class IntegrityCodesEnum(StrEnum):
    """
    Integrity error codes enum.
    """
    UNIQUE_VIOLATION = "23505"
    FOREIGN_KEY_VIOLATION = "23503"
    CHECK_VIOLATION = "23514"
    NOT_NULL_VIOLATION = "23502"

class RepositoryOperationsEnum(StrEnum):
    """
    Repository operation types.
    """
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
