#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field

from domain.value_objects import (
    LoaderName,
    LoaderVersion
)


@dataclass(slots=True)
class LoaderEntity:
    id: int
    game_id: int
    name: LoaderName
    versions: List[LoaderVersion]
    created_at: datetime
    updated_at: datetime

@dataclass(slots=True)
class LoaderCreateEntity:
    name: LoaderName
    versions: List[LoaderVersion]

@dataclass(slots=True)
class LoaderUpdateEntity:
    id: int
    name: Optional[LoaderName] = None
    versions: List[LoaderVersion] = field(default_factory=list)