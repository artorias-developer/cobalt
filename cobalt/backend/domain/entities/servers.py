#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List, Literal
from dataclasses import dataclass

from domain.value_objects import (
    ServerName,
    ServerVersion
)
from domain.entities.games import GameEntity
from domain.entities.loaders import LoaderEntity
from domain.entities.attributes import AttributeEntity
from domain.enums import ServerStatusEnum


@dataclass(slots=True)
class ServerEntity:
    id: int
    name: ServerName
    version: ServerVersion
    game: GameEntity
    loader: LoaderEntity
    attributes: List[AttributeEntity]
    status: ServerStatusEnum
    created_at: datetime
    updated_at: datetime

@dataclass(slots=True)
class ServersPageEntity:
    servers: List[ServerEntity]
    total: int
    page: int
    pages: int

@dataclass(slots=True)
class ServersGetPageEntity:
    page: int = 1
    search: Optional[str] = None
    sort_field: Literal["id", "name", "game_id", "loader_id", "version", "created_at", "updated_at"] = "id"
    sort_direction: Literal["asc", "desc"] = "desc"
    limit: int = 10

@dataclass(slots=True)
class ServerCreateEntity:
    name: ServerName
    game_id: int
    loader_id: int
    version: ServerVersion

@dataclass(slots=True)
class ServerUpdateEntity:
    id: int
    name: Optional[ServerName] = None
    version: Optional[ServerVersion] = None
    status: Optional[ServerStatusEnum] = None
