#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.dtos.base import BaseDto


class LogDto(BaseDto):
    message: str

class LogsSubscribeServerDto(BaseDto):
    server_id: int

class LogsUnsubscribeServerDto(BaseDto):
    server_id: int
