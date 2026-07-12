#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List, Literal, Annotated

from pydantic import BaseModel, Field, ConfigDict, RootModel

from domain.enums import ServerStateEnum
from presentation.http.fastapi.v1.schemas.games import GameShortSchema
from presentation.http.fastapi.v1.schemas.loaders import LoaderShortSchema
from presentation.http.fastapi.v1.schemas.attributes import AttributeSchema


class ServerSchema(BaseModel):
    id: int = Field(
        ...,
        title="Server id",
        description="Server ID"
    )

    name: str = Field(
        ...,
        title="Server name",
        description="Server name"
    )

    version: str = Field(
        ...,
        title="Server version",
        description="Server version"
    )

    game: GameShortSchema = Field(
        ...,
        title="Games",
        description="Game object"
    )

    loader: LoaderShortSchema = Field(
        ...,
        title="Loaders",
        description="Loader object"
    )

    attributes: List[AttributeSchema] = Field(
        ...,
        title="Attributes",
        description="List of server attributes"
    )

    state: ServerStateEnum = Field(
        ...,
        title="Server state",
        description="Server state"
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
                "name": "Terraria Survival",
                "version": "1.4.5.6",
                "game": {
                    "id": 1,
                    "name": "terraria",
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-02T12:00:00"
                },
                "loader": {
                    "id": 2,
                    "game_id": 1,
                    "name": "vanilla",
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-02T12:00:00"
                },
                "attributes": [
                    {
                        "id": 1,
                        "server_id": 1,
                        "key": "max_players",
                        "value": "20",
                        "created_at": "2024-01-01T12:00:00",
                        "updated_at": "2024-01-02T12:00:00"
                    }
                ],
                "state": "created",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )

class ServersPageSchema(BaseModel):
    servers: List[ServerSchema] = Field(
        ...,
        title="Servers",
        description="List of servers"
    )

    total: int = Field(
        ...,
        title="Total",
        description="Total number of servers"
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
                "servers": [
                    {
                        "id": 1,
                        "name": "Terraria Survival",
                        "version": "1.4.5.6",
                        "game": {
                            "id": 1,
                            "name": "terraria",
                            "created_at": "2024-01-01T12:00:00",
                            "updated_at": "2024-01-02T12:00:00"
                        },
                        "loader": {
                            "id": 2,
                            "game_id": 1,
                            "name": "vanilla",
                            "created_at": "2024-01-01T12:00:00",
                            "updated_at": "2024-01-02T12:00:00"
                        },
                        "attributes": [
                            {
                                "id": 1,
                                "server_id": 1,
                                "key": "max_players",
                                "value": "20",
                                "created_at": "2024-01-01T12:00:00",
                                "updated_at": "2024-01-02T12:00:00"
                            }
                        ],
                        "state": "created",
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

class ServerStatusSchema(BaseModel):
    running: bool = Field(
        ...,
        title="Running",
        description="Whether the server is running"
    )

    port: Optional[int] = Field(
        None,
        title="Port",
        description="Host port"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "running": True,
                "port": 7777
            }
        }
    )

class ServersGetPageSchema(BaseModel):
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

    sort_field: Literal["id", "name", "game_id", "loader_id", "version", "created_at", "updated_at"] = Field(
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
                "search": "Terraria Survival",
                "sort_field": "id",
                "sort_direction": "desc",
                "limit": 10
            }
        }
    )

class ServerCreateSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=128,
        pattern=r"^[a-zA-Zа-яА-ЯёЁіІїЇєЄ0-9_\-' ]+$",
        title="Server name",
        description="Server name"
    )

    game_id: int = Field(
        ...,
        gt=0,
        title="Game id",
        description="Game ID"
    )

    loader_id: int = Field(
        ...,
        gt=0,
        title="Loader id",
        description="Loader ID"
    )

    version: str = Field(
        ...,
        min_length=1,
        max_length=16,
        title="Server version",
        description="Server version"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "Terraria Survival",
                "game_id": 1,
                "loader_id": 2,
                "version": "1.4.5.6"
            }
        }
    )

class ServerUpdateSchema(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=128,
        pattern=r"^[a-zA-Zа-яА-ЯёЁіІїЇєЄ0-9_\-' ]+$",
        title="Server name",
        description="Server name"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "Terraria Survival Updated"
            }
        }
    )

class ServerUpgradeSchema(BaseModel):
    version: str = Field(
        ...,
        min_length=1,
        max_length=16,
        title="Server version",
        description="Server version"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "version": "1.4.5.6"
            }
        }
    )

class ServersDeleteSchema(RootModel):
    root: List[Annotated[int, Field(gt=0)]] = Field(
        ...,
        min_length=1,
        max_length=100,
        title="Server ids",
        description="List of server IDs to delete"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": [1, 2, 3]
        }
    )

class ServerExecuteSchema(BaseModel):
    command: str = Field(
        ...,
        min_length=1,
        max_length=1024,
        title="Command",
        description="Command to execute"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "command": "say Hello"
            }
        }
    )