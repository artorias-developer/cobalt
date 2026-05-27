#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional

from application.dtos.base import BaseDto


class AuthLoginDto(BaseDto):
    login: str
    password: str

class AuthSessionDto(BaseDto):
    session_id: str

class AuthChangeCredentialsDto(BaseDto):
    login: Optional[str] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None
