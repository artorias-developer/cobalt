#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, ConfigDict

from presentation.http.fastapi.v1.schemas.loaders import LoaderSchema


class GameSchema(BaseModel):
    id: int = Field(
        ...,
        title="Game id",
        description="Game ID"
    )

    name: str = Field(
        ...,
        title="Game name",
        description="Game name"
    )

    loaders: List[LoaderSchema] = Field(
        ...,
        title="Loaders",
        description="List of available loaders for this game"
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
                "name": "minecraft",
                "loaders": [
                    {
                        "id": 1,
                        "game_id": 1,
                        "name": "fabric",
                        "versions": ["1.20.1", "1.19.4", "1.18.2"],
                        "created_at": "2024-01-01T12:00:00",
                        "updated_at": "2024-01-02T12:00:00"
                    }
                ],
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )

class GameShortSchema(BaseModel):
    id: int = Field(
        ...,
        title="Game id",
        description="Game ID"
    )

    name: str = Field(
        ...,
        title="Game name",
        description="Game name"
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
                "name": "minecraft",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )

class GamesPageSchema(BaseModel):
    games: List[GameSchema] = Field(
        ...,
        title="Games",
        description="List of games"
    )

    total: int = Field(
        ...,
        title="Total",
        description="Total number of games"
    )

    page: int = Field(
        ...,
        title="Page",
        description="Current page"
    )

    pages: int = Field(
        ...,
        description="Total number of pages",
        title="Pages"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "games": [
                    {
                        "id": 1,
                        "name": "minecraft",
                        "loaders": [
                            {
                                "id": 1,
                                "game_id": 1,
                                "name": "fabric",
                                "versions": ["1.20.1", "1.19.4", "1.18.2"],
                                "created_at": "2024-01-01T12:00:00",
                                "updated_at": "2024-01-02T12:00:00"
                            }
                        ],
                        "created_at": "2024-01-01T12:00:00",
                        "updated_at": "2024-01-02T12:00:00"
                    }
                ],
                "total": 50,
                "page": 1,
                "pages": 5
            }
        }
    )

class GamesGetPageSchema(BaseModel):
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

    sort_field: Literal["id", "name", "loader_id", "created_at", "updated_at"] = Field(
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
                "search": "Minecraft",
                "sort_field": "id",
                "sort_direction": "desc",
                "limit": 10
            }
        }
    )