#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class MetricPoint:
    value: float
    date: datetime
