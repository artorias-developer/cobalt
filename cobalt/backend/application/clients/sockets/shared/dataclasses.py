#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass, field
from typing import Any, Dict

from orjson import loads


@dataclass
class SocketResponse:
    """
    Buffered response of a socket request.
    """
    status: int
    body: bytes = b""
    headers: Dict[str, str] = field(default_factory=dict)

    def json(self) -> Any:
        """
        Parses the body as JSON.

        Parameters:
        - None.

        Returns:
        - Any: Parsed JSON or None for an empty body.
        """
        if not self.body:
            return None

        return loads(self.body)

    def text(self) -> str:
        """
        Decodes the body as text.

        Parameters:
        - None.

        Returns:
        - str: Body text.
        """
        return self.body.decode("utf-8", errors="replace")