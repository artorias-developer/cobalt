#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from domain.value_objects import AbstractStrValueObject


class RoleName(AbstractStrValueObject):
    """
    Role name value object.
    """
    _MIN_LENGTH = 3
    _MAX_LENGTH = 32

    def _validate(self, value: str) -> None:
        """
        Validates the role name.

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