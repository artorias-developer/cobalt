#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass
from ipaddress import ip_address
from typing import ClassVar

from domain.exceptions import ValidationError
from domain.value_objects import AbstractValueObject


@dataclass(frozen=True, slots=True)
class IpAddress(AbstractValueObject):
    """
    IP address value object.
    """
    value: str

    _MAX_LENGTH: ClassVar[int] = 64

    def _validate(self) -> None:
        """
        Validates the IP address.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        self._validate_length(
            value=self.value,
            max_length=self._MAX_LENGTH
        )

        self._validate_ip_address(
            value=self.value
        )

    @staticmethod
    def _validate_ip_address(
        value: str
    ) -> None:
        """
        Validates that the value is a correct IPv4 or IPv6 address.

        Parameters:
        - value: Value to validate.

        Returns:
        - None.
        """
        try:
            ip_address(value)
        except ValueError as error:
            raise ValidationError('Invalid IP address "{ip_address}"', ip_address=value) from error
