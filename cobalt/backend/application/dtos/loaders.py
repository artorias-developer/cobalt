#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from application.dtos.base import BaseDto


class LoaderDto(BaseDto):
    id: int
    game_id: int
    name: str
    versions: List[str]
    created_at: datetime
    updated_at: datetime

class LoaderCreateDto(BaseDto):
    name: str
    versions: List[str]

class LoaderUpdateDto(BaseDto):
    id: int
    name: Optional[str] = None
    versions: List[str] = Field(default_factory=list)
