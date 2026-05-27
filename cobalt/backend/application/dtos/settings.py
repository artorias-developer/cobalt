#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional

from domain.enums import LanguageEnum, ThemeEnum, TimezoneEnum
from application.dtos.base import BaseDto


class SettingsDto(BaseDto):
    id: int
    user_id: int
    language: LanguageEnum
    theme: ThemeEnum
    timezone: TimezoneEnum
    created_at: datetime
    updated_at: datetime

class SettingsUpdateDto(BaseDto):
    language: Optional[LanguageEnum] = None
    theme: Optional[ThemeEnum] = None
    timezone: Optional[TimezoneEnum] = None