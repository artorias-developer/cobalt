#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass


@dataclass(slots=True)
class ContainerLog:
    message: str

@dataclass(slots=True)
class ContainerStatus:
    running: bool
    port: int