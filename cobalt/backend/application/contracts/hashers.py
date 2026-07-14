#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod


class AbstractHasher(ABC):
    """
    Abstract hasher.
    """

    @abstractmethod
    def generate_salt(
        self,
        length: int = 32
    ) -> str:
        """
        Generates a random hex salt of given length in bytes.

        Parameters:
        - length: Length in bytes.

        Returns:
        - str: Hex salt.
        """
        ...

    @abstractmethod
    def hash(
        self,
        plain: str,
        salt: str
    ) -> str:
        """
        Hashes a plain text.

        Parameters:
        - plain: Plain text to hash.
        - salt: Secret salt.

        Returns:
        - str: Hashed text.
        """
        ...

    @abstractmethod
    def verify(
        self,
        plain: str,
        hashed: str,
        salt: str
    ) -> bool:
        """
        Verifies a plain text against the hash.

        Parameters:
        - plain: Plain text to verify.
        - hashed: Hashed version of the plain text.
        - salt: Secret salt.

        Returns:
        - bool: True if plain text matches hash.
        """
        ...
