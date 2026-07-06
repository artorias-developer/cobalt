#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .base import BaseError

from .errors import (
    UnexpectedError,
    ValidationError,
    AuthenticationError,
    PermissionsError,
    NotFoundError,
    ConflictError
)

__all__ = [
    "BaseError",
    "UnexpectedError",
    "ValidationError",
    "AuthenticationError",
    "PermissionsError",
    "NotFoundError",
    "ConflictError"
]
