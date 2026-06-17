#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional, Literal, Annotated

from pydantic import BaseModel, Field, ConfigDict, RootModel

from presentation.http.fastapi.v1.schemas.roles import RoleSchema
from presentation.http.fastapi.v1.schemas.settings import SettingsSchema


class UserSchema(BaseModel):
    id: int = Field(
        ...,
        title="User id",
        description="User ID"
    )

    login: str = Field(
        ...,
        title="Login",
        description="User login"
    )

    role: RoleSchema = Field(
        ...,
        title="Roles",
        description="User role object"
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
                "login": "john_doe",
                "role": {
                    "id": 1,
                    "name": "admin",
                    "permissions": [
                        "users_view",
                        "users_create",
                        "roles_update"
                    ],
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-02T12:00:00"
                },
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )

class UserMeSchema(BaseModel):
    id: int = Field(
        ...,
        title="User id",
        description="User ID"
    )

    login: str = Field(
        ...,
        title="Login",
        description="User login"
    )

    role: RoleSchema = Field(
        ...,
        title="Roles",
        description="User role object"
    )

    settings: SettingsSchema = Field(
        ...,
        title="Settings",
        description="User settings"
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
                "login": "john_doe",
                "role": {
                    "id": 1,
                    "name": "admin",
                    "permissions": ["users_view"],
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-02T12:00:00"
                },
                "settings": {
                    "id": 1,
                    "language": "english",
                    "theme": "dark",
                    "timezone": "UTC",
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-02T12:00:00"
                },
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )

class UsersPageSchema(BaseModel):
    users: List[UserSchema] = Field(
        ...,
        title="Users",
        description="List of users"
    )

    total: int = Field(
        ...,
        title="Total",
        description="Total number of users"
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
                "users": [
                    {
                        "id": 1,
                        "login": "john_doe",
                        "role": {
                            "id": 1,
                            "name": "admin",
                            "permissions": [
                                "users_view",
                                "users_create",
                                "roles_update"
                            ],
                            "created_at": "2024-01-01T12:00:00",
                            "updated_at": "2024-01-02T12:00:00"
                        },
                        "created_at": "2024-01-01T12:00:00",
                        "updated_at": "2024-01-02T12:00:00"
                    }
                ],
                "total": 100,
                "page": 1,
                "pages": 10
            }
        }
    )

class UsersGetPageSchema(BaseModel):
    page: int = Field(
        1,
        gt=0,
        title="Page",
        description="Page number"
    )

    search: Optional[str] = Field(
        None,
        max_length=100,
        title="Search",
        description="Search query"
    )

    sort_field: Literal["id", "login", "role_id", "created_at", "updated_at"] = Field(
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
                "search": "john",
                "sort_field": "id",
                "sort_direction": "desc",
                "limit": 10
            }
        }
    )

class UserCreateSchema(BaseModel):
    login: str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_-]+$",
        title="Login",
        description="User login"
    )

    password: str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9!@#$%&*]+$",
        title="Password",
        description="User password"
    )

    role_id: int = Field(
        ...,
        gt=0,
        title="Role id",
        description="User role ID"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "login": "john_doe",
                "password": "SecurePass123",
                "role_id": 1
            }
        }
    )

class UserUpdateSchema(BaseModel):
    login: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Login",
        description="User login"
    )

    password: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9!@#$%&*]+$",
        title="Password",
        description="User password"
    )

    role_id: Optional[int] = Field(
        None,
        gt=0,
        title="Role id",
        description="User role ID"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "login": "john_doe_updated",
                "password": "NewSecurePass123",
                "role_id": 2
            }
        }
    )

class UsersDeleteSchema(RootModel):
    root: List[Annotated[int, Field(gt=0)]] = Field(
        ...,
        min_length=1,
        title="User ids",
        description="List of user IDs to delete"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": [1, 2, 3]
        }
    )