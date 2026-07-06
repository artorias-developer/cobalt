#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional, Literal
from dataclasses import dataclass

from domain.value_objects import AttributeKey


@dataclass(slots=True)
class AttributeEntity:
    id: int
    server_id: int
    key: AttributeKey
    value: str
    created_at: datetime
    updated_at: datetime

@dataclass(slots=True)
class AttributesPageEntity:
    attributes: List[AttributeEntity]
    total: int
    page: int
    pages: int

@dataclass(slots=True)
class AttributesGetPageEntity:
    page: int = 1
    search: Optional[str] = None
    sort_field: Literal["id", "key", "value", "created_at", "updated_at"] = "id"
    sort_direction: Literal["asc", "desc"] = "desc"
    limit: int = 10

@dataclass(slots=True)
class AttributeCreateEntity:
    key: AttributeKey
    value: str

@dataclass(slots=True)
class AttributeUpdateEntity:
    id: int
    key: Optional[AttributeKey] = None
    value: Optional[str] = None