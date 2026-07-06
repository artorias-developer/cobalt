#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass
from re import compile as re_compile
from typing import ClassVar, Pattern

from domain.value_objects import AbstractValueObject


@dataclass(frozen=True, slots=True)
class GameName(AbstractValueObject):
    """
    Game name value object.
    """
    value: str

    _PATTERN: ClassVar[Pattern] = re_compile(r"^[a-z_]+$")
    _MIN_LENGTH: ClassVar[int] = 1
    _MAX_LENGTH: ClassVar[int] = 32

    def _validate(self) -> None:
        """
        Validates the game name.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        self._validate_length(
            value=self.value,
            min_length=self._MIN_LENGTH,
            max_length=self._MAX_LENGTH
        )

        self._validate_pattern(
            value=self.value,
            pattern=self._PATTERN
        )