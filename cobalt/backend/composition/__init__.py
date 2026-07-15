#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .containers.fastapi import setup_fastapi_ioc_container, setup_fastapi_app
from .dataclasses import ApplicationContainer

__all__ = [
    "setup_fastapi_ioc_container",
    "setup_fastapi_app",
    "ApplicationContainer"
]