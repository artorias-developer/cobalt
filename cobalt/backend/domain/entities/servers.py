#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

from domain.enums import (
    ServerStateEnum,
    SortDirectionEnum,
    ServerSortFieldEnum
)
from domain.value_objects import (
    ServerName,
    LoaderVersion,
    PageLimit,
    Search
)
from domain.entities.games import GameEntity
from domain.entities.loaders import LoaderEntity
from domain.entities.attributes import AttributeEntity


@dataclass(slots=True)
class ServerEntity:
    id: int
    name: ServerName
    version: LoaderVersion
    game: GameEntity
    loader: LoaderEntity
    attributes: List[AttributeEntity]
    state: ServerStateEnum
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
    search: Optional[Search] = None
    sort_field: ServerSortFieldEnum = ServerSortFieldEnum.ID
    sort_direction: SortDirectionEnum = SortDirectionEnum.DESC
    limit: PageLimit = PageLimit(10)

@dataclass(slots=True)
class ServerCreateEntity:
    name: ServerName
    game_id: int
    loader_id: int
    version: LoaderVersion

@dataclass(slots=True)
class ServerUpdateEntity:
    id: int
    name: Optional[ServerName] = None
    version: Optional[LoaderVersion] = None
    state: Optional[ServerStateEnum] = None
