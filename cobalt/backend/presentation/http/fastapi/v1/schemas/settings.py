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
        description="Settings ID"
    )

    user_id: int = Field(
        ...,
        description="Settings user ID"
    )

    language: LanguageEnum = Field(
        ...,
        description="Language"
    )

    theme: ThemeEnum = Field(
        ...,
        description="Theme"
    )

    timezone: TimezoneEnum = Field(
        ...,
        description="Timezone"
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
        description="Language"
    )

    theme: Optional[ThemeEnum] = Field(
        None,
        description="Theme"
    )

    timezone: Optional[TimezoneEnum] = Field(
        None,
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