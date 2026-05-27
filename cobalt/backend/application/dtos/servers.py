#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional, Literal

from domain.enums import ServerStatusEnum
from application.dtos.base import BaseDto
from application.dtos.games import GameDto
from application.dtos.loaders import LoaderDto
from application.dtos.attributes import AttributeDto


class ServerDto(BaseDto):
    id: int
    name: str
    version: str
    game: GameDto
    loader: LoaderDto
    attributes: List[AttributeDto]
    status: ServerStatusEnum
    created_at: datetime
    updated_at: datetime

class ServersPageDto(BaseDto):
    servers: List[ServerDto]
    total: int
    page: int
    pages: int

class ServerStatusDto(BaseDto):
    running: bool
    port: Optional[int] = None

class ServersGetPageDto(BaseDto):
    page: int
    search: Optional[str] = None
    sort_field: Literal["id", "name", "game_id", "loader_id", "version", "created_at", "updated_at"] = "id"
    sort_direction: Literal["asc", "desc"] = "desc"
    limit: int = 10

class ServerCreateDto(BaseDto):
    name: str
    game_id: int
    loader_id: int
    version: str

class ServerUpdateDto(BaseDto):
    name: Optional[str] = None
    status: Optional[ServerStatusEnum] = None

class ServerExecuteDto(BaseDto):
    command: str
