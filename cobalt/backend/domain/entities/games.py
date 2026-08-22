#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from domain.enums import (
    SortDirectionEnum,
    GameSortFieldEnum
)
from domain.value_objects import (
    GameName,
    PageLimit,
    Search
)
from domain.entities.loaders import LoaderEntity


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
    search: Optional[Search] = None
    sort_field: GameSortFieldEnum = GameSortFieldEnum.ID
    sort_direction: SortDirectionEnum = SortDirectionEnum.DESC
    limit: PageLimit = PageLimit(10)

@dataclass(slots=True)
class GameCreateEntity:
    name: GameName

@dataclass(slots=True)
class GameUpdateEntity:
    id: int
    name: GameName