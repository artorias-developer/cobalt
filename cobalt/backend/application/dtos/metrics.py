#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime

from application.dtos.base import BaseDto


class MetricDto(BaseDto):
    value: float
    date: datetime

class MetricDiskDto(BaseDto):
    free: int
    total: int
    last_check: datetime
    next_check: datetime

class MetricsSubscribeServerDto(BaseDto):
    server_id: int

class MetricsUnsubscribeServerDto(BaseDto):
    server_id: int
