#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List, Literal
from dataclasses import dataclass

from domain.value_objects import (
    UserLogin,
    HashedPassword,
    Salt
)
from domain.entities.roles import RoleEntity
from domain.entities.settings import SettingsEntity


@dataclass(slots=True)
class UserEntity:
    id: int
    login: UserLogin
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
    search: Optional[str] = None
    sort_field: Literal["id", "login", "role_id", "created_at", "updated_at"] = "id"
    sort_direction: Literal["asc", "desc"] = "desc"
    limit: int = 10

@dataclass(slots=True)
class UserCreateEntity:
    login: UserLogin
    hashed_password: HashedPassword
    salt: Salt
    role_id: int

@dataclass(slots=True)
class UserUpdateEntity:
    id: int
    login: Optional[UserLogin] = None
    hashed_password: Optional[HashedPassword] = None
    salt: Optional[Salt] = None
    role_id: Optional[int] = None
