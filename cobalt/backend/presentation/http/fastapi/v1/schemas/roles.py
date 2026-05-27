#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List, Literal, Annotated

from pydantic import BaseModel, Field, ConfigDict, RootModel

from domain.enums import PermissionsEnum


class RoleSchema(BaseModel):
    id: int = Field(
        ...,
        description="Role ID"
    )

    name: str = Field(
        ...,
        description="Role name"
    )

    permissions: List[PermissionsEnum] = Field(
        ...,
        description="List of permissions"
    )

    created_at: datetime = Field(
        ...,
        description="Creation timestamp"
    )

    updated_at: datetime = Field(
        ...,
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
        description="List of roles"
    )

    total: int = Field(
        ...,
        description="Total number of roles"
    )

    page: int = Field(
        ...,
        description="Current page"
    )

    pages: int = Field(
        ...,
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
        description="Page number"
    )

    search: Optional[str] = Field(
        None,
        max_length=100,
        description="Search query"
    )

    sort_field: Literal["id", "name", "created_at", "updated_at"] = Field(
        "id",
        description="Field to sort by"
    )

    sort_direction: Literal["asc", "desc"] = Field(
        "desc",
        description="Sort direction"
    )

    limit: int = Field(
        10,
        gt=0,
        le=100,
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
        description="Role name"
    )

    permissions: List[PermissionsEnum] = Field(
        ...,
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
        description="Role name"
    )

    permissions: Optional[List[PermissionsEnum]] = Field(
        None,
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
        description="List of role IDs to delete"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": [1, 2, 3]
        }
    )