#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class AuthLoginSchema(BaseModel):
    login: str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Zа-яА-ЯёЁіІїЇєЄ0-9_\-' ]+$",
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

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "login": "john_doe",
                "password": "SecurePass123"
            }
        }
    )

class AuthChangeCredentialsSchema(BaseModel):
    login: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Zа-яА-ЯёЁіІїЇєЄ0-9_\-' ]+$",
        title="Login",
        description="New login"
    )

    old_password: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9!@#$%&*]+$",
        title="Old password",
        description="Current password"
    )

    new_password: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9!@#$%&*]+$",
        title="New password",
        description="New password"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "login": "new_login",
                "old_password": "OldPass123",
                "new_password": "NewPass123"
            }
        }
    )
