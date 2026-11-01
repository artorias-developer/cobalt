#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional


class SocketError(Exception):
    """
    Raised when the socket request fails: connection problems or an HTTP error status in a streamed response.
    """
    status: Optional[int]
    message: str

    def __init__(
        self,
        message: str,
        status: Optional[int] = None
    ):
        super().__init__(message)

        self.message = message
        self.status = status