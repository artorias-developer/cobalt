#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from re import compile as re_compile

from domain.value_objects import AbstractStrValueObject


class LoaderName(AbstractStrValueObject):
    """
    Loader name value object.
    """
    _PATTERN = re_compile(r"^[a-z_]+$")
    _MIN_LENGTH = 1
    _MAX_LENGTH = 32

    def _validate(self, value: str) -> None:
        """
        Validates the loader name.

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