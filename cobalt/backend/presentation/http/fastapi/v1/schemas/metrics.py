#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class MetricSchema(BaseModel):
    value: float = Field(
        ...,
        title="Value",
        description="Metric value"
    )

    date: datetime = Field(
        ...,
        title="Date",
        description="Metric timestamp"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "value": 75.42,
                "date": "2024-01-02T12:00:00"
            }
        }
    )

class MetricDiskSchema(BaseModel):
    free: int = Field(
        ...,
        title="Free",
        description="Free disk space in bytes"
    )

    total: int = Field(
        ...,
        title="Total",
        description="Total disk space in bytes"
    )

    last_check: datetime = Field(
        ...,
        title="Last check",
        description="Last check timestamp"
    )

    next_check: datetime = Field(
        ...,
        title="Next check",
        description="Next check timestamp"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "free": 214748364800,
                "total": 536870912000,
                "last_check": "2024-01-02T12:00:00",
                "next_check": "2024-01-02T12:05:00"
            }
        }
    )
