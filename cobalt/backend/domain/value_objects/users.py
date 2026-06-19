#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from re import compile as re_compile

from domain.value_objects import AbstractStrValueObject


class UserLogin(AbstractStrValueObject):
    """
    User login value object.
    """
    _PATTERN = re_compile(r"^[a-zA-Zа-яА-ЯёЁіІїЇєЄ0-9_\-' ]+$")
    _MIN_LENGTH = 3
    _MAX_LENGTH = 32

    def _validate(self, value: str) -> None:
        """
        Validates the user login.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        self._validate_length(
            value=value,
            min_length=self._MIN_LENGTH,
            max_length=self._MAX_LENGTH
        )

        self._validate_pattern(
            value=value,
            pattern=self._PATTERN
        )

class HashedPassword(AbstractStrValueObject):
    """
    Hashed password value object.
    """
    _MAX_LENGTH = 128

    def _validate(self, value: str) -> None:
        """
        Validates the hashed password.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        self._validate_length(
            value=value,
            max_length=self._MAX_LENGTH
        )

class Salt(AbstractStrValueObject):
    """
    Salt value object.
    """
    _MAX_LENGTH = 128

    def _validate(self, value: str) -> None:
        """
        Validates the salt.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        self._validate_length(
            value=value,
            max_length=self._MAX_LENGTH
        )