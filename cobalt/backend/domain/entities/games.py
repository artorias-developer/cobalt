#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Literal, Optional
from dataclasses import dataclass

from domain.entities.loaders import LoaderEntity
from domain.value_objects import GameName


@dataclass(slots=True)
class GameEntity:
    id: int
    name: GameName
    loaders: List[LoaderEntity]
    created_at: datetime
    updated_at: datetime

@dataclass(slots=True)
class GamesPageEntity:
    games: List[GameEntity]
    total: int
    page: int
    pages: int

@dataclass(slots=True)
class GamesGetPageEntity:
    page: int
    search: Optional[str] = None
    sort_field: Literal["id", "name", "loader_id", "created_at", "updated_at"] = "id"
    sort_direction: Literal["asc", "desc"] = "desc"
    limit: int = 10

@dataclass(slots=True)
class GameCreateEntity:
    name: GameName

@dataclass(slots=True)
class GameUpdateEntity:
    id: int
    name: GameName