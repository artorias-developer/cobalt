#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional, Literal
from dataclasses import dataclass, field

from domain.value_objects import RoleName
from domain.enums import PermissionsEnum


@dataclass(slots=True)
class RoleEntity:
    id: int
    name: RoleName
    permissions: List[PermissionsEnum]
    created_at: datetime
    updated_at: datetime

@dataclass(slots=True)
class RolesPageEntity:
    roles: List[RoleEntity]
    total: int
    page: int
    pages: int

@dataclass(slots=True)
class RolesGetPageEntity:
    page: int = 1
    search: Optional[str] = None
    sort_field: Literal["id", "name", "created_at", "updated_at"] = "id"
    sort_direction: Literal["asc", "desc"] = "desc"
    limit: int = 10

@dataclass(slots=True)
class RoleCreateEntity:
    name: RoleName
    permissions: List[PermissionsEnum]

@dataclass(slots=True)
class RoleUpdateEntity:
    id: int
    name: Optional[RoleName] = None
    permissions: List[PermissionsEnum] = field(default_factory=list)
