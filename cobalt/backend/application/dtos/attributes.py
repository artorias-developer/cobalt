#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List

from application.dtos.base import BaseDto
from domain.enums import SortDirectionEnum, AttributeSortFieldEnum


class AttributeDto(BaseDto):
    id: int
    server_id: int
    key: str
    value: str
    created_at: datetime
    updated_at: datetime

class AttributesPageDto(BaseDto):
    attributes: List[AttributeDto]
    total: int
    page: int
    pages: int

class AttributesGetPageDto(BaseDto):
    page: int
    search: Optional[str] = None
    sort_field: AttributeSortFieldEnum = AttributeSortFieldEnum.ID
    sort_direction: SortDirectionEnum = SortDirectionEnum.DESC
    limit: int = 10

class AttributeCreateDto(BaseDto):
    key: str
    value: str

class AttributeUpdateDto(BaseDto):
    id: int
    key: Optional[str] = None
    value: Optional[str] = None
