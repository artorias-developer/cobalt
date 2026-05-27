#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from domain.exceptions import BaseError


class UnexpectedError(BaseError):
    ...

class ValidationError(BaseError):
    ...

class AuthenticationError(BaseError):
    ...

class PermissionsError(BaseError):
    ...

class NotFoundError(BaseError):
    ...

class ConflictError(BaseError):
    ...
