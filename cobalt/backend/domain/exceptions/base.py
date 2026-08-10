#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any


class BaseError(Exception):
    error_message: str
    kwargs: Any

    def __init__(
        self,
        error_message: str,
        **kwargs: Any
    ):
        self.error_message = error_message
        self.kwargs = kwargs
        super().__init__(error_message.format(**kwargs))