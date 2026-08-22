#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field

from domain.enums import (
    PermissionEnum,
    SortDirectionEnum,
    RoleSortFieldEnum
)
from domain.value_objects import (
    RoleName,
    PageLimit,
    Search
)


@dataclass(slots=True)
class RoleEntity:
    id: int
    name: RoleName
    permissions: List[PermissionEnum]
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
    search: Optional[Search] = None
    sort_field: RoleSortFieldEnum = RoleSortFieldEnum.ID
    sort_direction: SortDirectionEnum = SortDirectionEnum.DESC
    limit: PageLimit = PageLimit(10)

@dataclass(slots=True)
class RoleCreateEntity:
    name: RoleName
    permissions: List[PermissionEnum]

@dataclass(slots=True)
class RoleUpdateEntity:
    id: int
    name: Optional[RoleName] = None
    permissions: List[PermissionEnum] = field(default_factory=list)
