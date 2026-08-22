#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

from domain.enums import (
    SortDirectionEnum,
    UserSortFieldEnum
)
from domain.value_objects import (
    Login,
    HashedPassword,
    Salt,
    PageLimit,
    Search
)
from domain.entities.roles import RoleEntity
from domain.entities.settings import SettingsEntity


@dataclass(slots=True)
class UserEntity:
    id: int
    login: Login
    hashed_password: HashedPassword
    salt: Salt
    role: RoleEntity
    settings: SettingsEntity
    created_at: datetime
    updated_at: datetime

@dataclass(slots=True)
class UsersPageEntity:
    users: List[UserEntity]
    total: int
    page: int
    pages: int

@dataclass(slots=True)
class UsersGetPageEntity:
    page: int = 1
    search: Optional[Search] = None
    sort_field: UserSortFieldEnum = UserSortFieldEnum.ID
    sort_direction: SortDirectionEnum = SortDirectionEnum.DESC
    limit: PageLimit = PageLimit(10)

@dataclass(slots=True)
class UserCreateEntity:
    login: Login
    hashed_password: HashedPassword
    salt: Salt
    role_id: int

@dataclass(slots=True)
class UserUpdateEntity:
    id: int
    login: Optional[Login] = None
    hashed_password: Optional[HashedPassword] = None
    salt: Optional[Salt] = None
    role_id: Optional[int] = None
