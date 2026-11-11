#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass
from typing import ClassVar, TypeVar, List, Generic

from domain.value_objects import AbstractValueObject


T = TypeVar("T")

@dataclass(frozen=True, slots=True)
class Search(AbstractValueObject):
    """
    Search query value object.
    """
    value: str

    _MIN_LENGTH: ClassVar[int] = 1
    _MAX_LENGTH: ClassVar[int] = 128

    def _validate(self) -> None:
        """
        Validates the search query.

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

@dataclass(frozen=True, slots=True)
class PageLimit(AbstractValueObject):
    """
    Pagination page limit value object.
    """
    value: int

    _MIN_VALUE: ClassVar[int] = 1
    _MAX_VALUE: ClassVar[int] = 100

    def _validate(self) -> None:
        """
        Validates the page limit value.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        self._validate_range(
            value=self.value,
            min_value=self._MIN_VALUE,
            max_value=self._MAX_VALUE
        )

@dataclass(frozen=True, slots=True)
class Batch(AbstractValueObject, Generic[T]):
    """
    Batch of items value object.
    """
    value: List[T]

    _MIN_SIZE: ClassVar[int] = 1
    _MAX_SIZE: ClassVar[int] = 100

    def _validate(self) -> None:
        """
        Validates the batch size.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        self._validate_size(
            value=self.value,
            min_size=self._MIN_SIZE,
            max_size=self._MAX_SIZE
        )
