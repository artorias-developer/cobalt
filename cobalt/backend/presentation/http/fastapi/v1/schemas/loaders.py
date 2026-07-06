#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict


class LoaderSchema(BaseModel):
    id: int = Field(
        ...,
        title="Loader id",
        description="Loader ID"
    )

    game_id: int = Field(
        ...,
        title="Game id",
        description="Game ID"
    )

    name: str = Field(
        ...,
        title="Loader name",
        description="Loader name"
    )

    versions: List[str] = Field(
        ...,
        title="Versions",
        description="List of supported versions"
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
                "game_id": 1,
                "name": "fabric",
                "versions": ["1.20.1", "1.19.4", "1.18.2"],
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )

class LoaderShortSchema(BaseModel):
    id: int = Field(
        ...,
        title="Loader id",
        description="Loader ID"
    )

    game_id: int = Field(
        ...,
        title="Game id",
        description="Game ID"
    )

    name: str = Field(
        ...,
        title="Loader name",
        description="Loader name"
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
                "game_id": 1,
                "name": "fabric",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )
