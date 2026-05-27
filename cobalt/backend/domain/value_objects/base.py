from re import Pattern
from typing import Optional
from abc import ABC, abstractmethod


class AbstractStrValueObject(str, ABC):
    """
    Abstract string value object.
    """

    def __new__(cls, value: str):
        instance = super().__new__(cls, value)
        instance._validate(value)
        return instance

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
    def _validate(self, value: str) -> None:
        """
        Validates the value object.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        ...