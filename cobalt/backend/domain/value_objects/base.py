#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from dataclasses import dataclass
from re import Pattern
from typing import Optional, TypeVar

from domain.exceptions import ValidationError

Number = TypeVar("Number", int, float)


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
            raise ValidationError(
                '"{value}" must be at least {min_length} characters',
                value=value,
                min_length=min_length
            )

        if max_length is not None and len(value) > max_length:
            raise ValidationError(
                '"{value}" must be at most {max_length} characters',
                value=value,
                max_length=max_length
            )

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
            raise ValidationError(
                '"{value}" must match pattern {pattern}',
                value=value,
                pattern=pattern.pattern
            )

    @staticmethod
    def _validate_range(
        value: Number,
        min_value: Optional[Number] = None,
        max_value: Optional[Number] = None
    ) -> None:
        """
        Validates that the value is within the given range (inclusive).

        Parameters:
        - value: Value to validate.
        - min_value: Minimum allowed value (inclusive).
        - max_value: Maximum allowed value (inclusive).

        Returns:
        - None.
        """
        if min_value is not None and value < min_value:
            raise ValidationError(
                '"{value}" must be at least {min_value}',
                value=value,
                min_value=min_value
            )

        if max_value is not None and value > max_value:
            raise ValidationError(
                '"{value}" must be at most {max_value}',
                value=value,
                max_value=max_value
            )

    @staticmethod
    def _validate_greater_than(
        value: Number,
        threshold: Number
    ) -> None:
        """
        Validates that the value is strictly greater than the threshold.

        Parameters:
        - value: Value to validate.
        - threshold: Value that must be exceeded.

        Returns:
        - None.
        """
        if value <= threshold:
            raise ValidationError(
                '"{value}" must be greater than {threshold}',
                value=value,
                threshold=threshold
            )

    @staticmethod
    def _validate_greater_than_or_equal(
        value: Number,
        threshold: Number
    ) -> None:
        """
        Validates that the value is greater than or equal to the threshold.

        Parameters:
        - value: Value to validate.
        - threshold: Minimum allowed value (inclusive).

        Returns:
        - None.
        """
        if value < threshold:
            raise ValidationError(
                '"{value}" must be greater than or equal to {threshold}',
                value=value,
                threshold=threshold
            )

    @staticmethod
    def _validate_less_than(
        value: Number,
        threshold: Number
    ) -> None:
        """
        Validates that the value is strictly less than the threshold.

        Parameters:
        - value: Value to validate.
        - threshold: Value that the input must be below.

        Returns:
        - None.
        """
        if value >= threshold:
            raise ValidationError(
                '"{value}" must be less than {threshold}',
                value=value,
                threshold=threshold
            )

    @staticmethod
    def _validate_less_than_or_equal(
        value: Number,
        threshold: Number
    ) -> None:
        """
        Validates that the value is less than or equal to the threshold.

        Parameters:
        - value: Value to validate.
        - threshold: Maximum allowed value (inclusive).

        Returns:
        - None.
        """
        if value > threshold:
            raise ValidationError(
                '"{value}" must be less than or equal to {threshold}',
                value=value,
                threshold=threshold
            )

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