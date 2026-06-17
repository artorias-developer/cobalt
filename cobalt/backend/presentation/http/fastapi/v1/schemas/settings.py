#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from domain.enums import (
    LanguageEnum,
    ThemeEnum,
    TimezoneEnum
)


class SettingsSchema(BaseModel):
    id: int = Field(
        ...,
        title="Settings id",
        description="Settings ID"
    )

    user_id: int = Field(
        ...,
        title="Settings user id",
        description="Settings user ID"
    )

    language: LanguageEnum = Field(
        ...,
        title="Language",
        description="Language"
    )

    theme: ThemeEnum = Field(
        ...,
        title="Theme",
        description="Theme"
    )

    timezone: TimezoneEnum = Field(
        ...,
        title="Timezone",
        description="Timezone"
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
                "user_id": 1,
                "language": "english",
                "theme": "dark",
                "timezone": "UTC",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )

class SettingsUpdateSchema(BaseModel):
    language: Optional[LanguageEnum] = Field(
        None,
        title="Language",
        description="Language"
    )

    theme: Optional[ThemeEnum] = Field(
        None,
        title="Theme",
        description="Theme"
    )

    timezone: Optional[TimezoneEnum] = Field(
        None,
        title="Timezone",
        description="Timezone"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "language": "english",
                "theme": "dark",
                "timezone": "UTC+2"
            }
        }
    )