#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List, Literal, Annotated

from pydantic import BaseModel, Field, ConfigDict, RootModel

from domain.enums import PermissionEnum


class RoleSchema(BaseModel):
    id: int = Field(
        ...,
        title="Role id",
        description="Role ID"
    )

    name: str = Field(
        ...,
        title="Role name",
        description="Role name"
    )

    permissions: List[PermissionEnum] = Field(
        ...,
        title="Permissions",
        description="List of permissions"
    )

    created_at: datetime = Field(
        ...,
        title="Created at",
        description="Creation timestamp"
    )

    updated_at: datetime = Field(
        ...,
        title="Updated at",
        description="Last update timestamp"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "admin",
                "permissions": [
                    "users_view",
                    "users_create",
                    "roles_update"
                ],
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )

class RolesPageSchema(BaseModel):
    roles: List[RoleSchema] = Field(
        ...,
        title="Roles",
        description="List of roles"
    )

    total: int = Field(
        ...,
        title="Total",
        description="Total number of roles"
    )

    page: int = Field(
        ...,
        title="Page",
        description="Current page"
    )

    pages: int = Field(
        ...,
        title="Pages",
        description="Total number of pages"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "roles": [
                    {
                        "id": 1,
                        "name": "admin",
                        "permissions": [
                            "users_view",
                            "users_create",
                            "roles_update"
                        ],
                        "created_at": "2024-01-01T12:00:00",
                        "updated_at": "2024-01-02T12:00:00"
                    }
                ],
                "total": 3,
                "page": 1,
                "pages": 1
            }
        }
    )

class RolesGetPageSchema(BaseModel):
    page: int = Field(
        1,
        gt=0,
        title="Page",
        description="Page number"
    )

    search: Optional[str] = Field(
        None,
        max_length=100,
        pattern=r"^[a-zA-Zа-яА-ЯёЁіІїЇєЄ0-9_\-.,' ]+$",
        title="Search",
        description="Search query"
    )

    sort_field: Literal["id", "name", "created_at", "updated_at"] = Field(
        "id",
        title="Sort field",
        description="Field to sort by"
    )

    sort_direction: Literal["asc", "desc"] = Field(
        "desc",
        title="Sort direction",
        description="Sort direction"
    )

    limit: int = Field(
        10,
        gt=0,
        le=100,
        title="Limit",
        description="Number of items per page"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "page": 1,
                "search": "admin",
                "sort_field": "id",
                "sort_direction": "desc",
                "limit": 10
            }
        }
    )

class RoleCreateSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Zа-яА-ЯёЁіІїЇєЄ0-9_\-' ]+$",
        title="Role name",
        description="Role name"
    )

    permissions: List[PermissionEnum] = Field(
        ...,
        title="Permissions",
        description="List of permissions"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "manager",
                "permissions": [
                    "users_view",
                    "servers_view"
                ]
            }
        }
    )

class RoleUpdateSchema(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Zа-яА-ЯёЁіІїЇєЄ0-9_\-' ]+$",
        title="Role name",
        description="Role name"
    )

    permissions: Optional[List[PermissionEnum]] = Field(
        None,
        title="Permissions",
        description="List of permissions"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "manager_updated",
                "permissions": [
                    "users_view",
                    "users_update"
                ]
            }
        }
    )

class RolesDeleteSchema(RootModel):
    root: List[Annotated[int, Field(gt=0)]] = Field(
        ...,
        min_length=1,
        title="Role ids",
        description="List of role IDs to delete"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": [1, 2, 3]
        }
    )