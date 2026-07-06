#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from domain.enums import (
    LanguageEnum,
    ThemeEnum,
    TimezoneEnum
)


@dataclass(slots=True)
class SettingsEntity:
    id: int
    user_id: int
    language: LanguageEnum
    theme: ThemeEnum
    timezone: TimezoneEnum
    created_at: datetime
    updated_at: datetime

@dataclass(slots=True)
class SettingsUpdateEntity:
    language: Optional[LanguageEnum] = None
    theme: Optional[ThemeEnum] = None
    timezone: Optional[TimezoneEnum] = None