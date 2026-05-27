#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass, field
from typing import Set, Dict, Any


@dataclass(slots=True)
class Room:
    connections: Set[int] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)