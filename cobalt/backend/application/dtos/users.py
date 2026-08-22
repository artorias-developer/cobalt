#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional

from domain.enums import (
    SortDirectionEnum,
    UserSortFieldEnum
)
from application.dtos.base import BaseDto
from application.dtos.roles import RoleDto
from application.dtos.settings import SettingsDto


class UserDto(BaseDto):
    id: int
    login: str
    hashed_password: str
    salt: str
    role: RoleDto
    settings: SettingsDto
    created_at: datetime
    updated_at: datetime

class UsersPageDto(BaseDto):
    users: List[UserDto]
    total: int
    page: int
    pages: int

class UsersGetPageDto(BaseDto):
    page: int
    search: Optional[str] = None
    sort_field: UserSortFieldEnum = UserSortFieldEnum.ID
    sort_direction: SortDirectionEnum = SortDirectionEnum.DESC
    limit: int = 10

class UserCreateDto(BaseDto):
    login: str
    password: str
    role_id: int

class UserUpdateDto(BaseDto):
    login: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
