#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List

from pydantic import Field

from domain.enums import (
    PermissionEnum,
    SortDirectionEnum,
    RoleSortFieldEnum
)
from application.dtos.base import BaseDto


class RoleDto(BaseDto):
    id: int
    name: str
    permissions: List[PermissionEnum]
    created_at: datetime
    updated_at: datetime

class RolesPageDto(BaseDto):
    roles: List[RoleDto]
    total: int
    page: int
    pages: int

class RolesGetPageDto(BaseDto):
    page: int
    search: Optional[str] = None
    sort_field: RoleSortFieldEnum = RoleSortFieldEnum.ID
    sort_direction: SortDirectionEnum = SortDirectionEnum.DESC
    limit: int = 10

class RoleCreateDto(BaseDto):
    name: str
    permissions: List[PermissionEnum]

class RoleUpdateDto(BaseDto):
    name: Optional[str] = None
    permissions: List[PermissionEnum] = Field(default_factory=list)
