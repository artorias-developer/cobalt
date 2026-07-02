#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from dataclasses import dataclass
from re import Pattern
from typing import Optional


@dataclass(frozen=True, slots=True)
class AbstractValueObject(ABC):
    """
    Abstract value object.
    """

    def __post_init__(self) -> None:
        self._validate()

    @staticmethod
    def _validate_length(
        value: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> None:
        """
        Validates the length of the value.

        Parameters:
        - value: Value to validate.
        - min_length: Minimum length.
        - max_length: Maximum length.

        Returns:
        - None.
        """
        if min_length is not None and len(value) < min_length:
            raise ValueError(f'"{value}" must be at least {min_length} characters')

        if max_length is not None and len(value) > max_length:
            raise ValueError(f'"{value}" must be at most {max_length} characters')

    @staticmethod
    def _validate_pattern(
        value: str,
        pattern: Pattern
    ) -> None:
        """
        Validates the value against a pattern.

        Parameters:
        - value: Value to validate.
        - pattern: Pattern to match.

        Returns:
        - None.
        """
        if not pattern.match(value):
            raise ValueError(f'"{value}" must match pattern {pattern.pattern}')

    @abstractmethod
    def _validate(self) -> None:
        """
        Validates the value object.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        ...