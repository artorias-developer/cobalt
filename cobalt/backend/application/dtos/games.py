#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional, Literal

from application.dtos.base import BaseDto
from application.dtos.loaders import LoaderDto


class GameDto(BaseDto):
    id: int
    name: str
    loaders: List[LoaderDto]
    created_at: datetime
    updated_at: datetime
    
class GamesPageDto(BaseDto):
    games: List[GameDto]
    total: int
    page: int
    pages: int

class GamesGetPageDto(BaseDto):
    page: int
    search: Optional[str] = None
    sort_field: Literal["id", "name", "loader_id", "created_at", "updated_at"] = "id"
    sort_direction: Literal["asc", "desc"] = "desc"
    limit: int = 10

class GameCreateDto(BaseDto):
    name: str

class GameUpdateDto(BaseDto):
    name: str
