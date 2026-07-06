#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel, Field, ConfigDict


class LogSchema(BaseModel):
    message: str = Field(
        ...,
        title="Message",
        description="Log message"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "message": "2026-02-03 18:26:46 [PID 1] INFO cobalt.app - Server started successfully."
            }
        }
    )