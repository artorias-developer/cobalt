#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field

from domain.value_objects import LoaderName


@dataclass(slots=True)
class LoaderEntity:
    id: int
    game_id: int
    name: LoaderName
    versions: List[str]
    created_at: datetime
    updated_at: datetime

@dataclass(slots=True)
class LoaderCreateEntity:
    name: LoaderName
    versions: List[str]

@dataclass(slots=True)
class LoaderUpdateEntity:
    id: int
    name: Optional[LoaderName] = None
    versions: List[str] = field(default_factory=list)