#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, model_validator

from domain.exceptions import ValidationError


class AuthLoginSchema(BaseModel):
    login: str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="User login"
    )

    password: str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9!@#$%&*]+$",
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
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="New login"
    )

    old_password: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9!@#$%&*]+$",
        description="Current password"
    )

    new_password: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9!@#$%&*]+$",
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

    @model_validator(mode="after")
    def validate_passwords(self) -> "AuthChangeCredentialsSchema":
        if bool(self.old_password) != bool(self.new_password):
            raise ValidationError("One of the passwords is missing")
        return self
