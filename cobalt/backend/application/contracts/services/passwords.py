#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod


class AbstractPasswordsService(ABC):
    """
    Abstract passwords service.
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
    def hash_password(
        self,
        password: str,
        local_salt: str
    ) -> str:
        """
        Hashes a password using local salt + global salt + SHA256 + bcrypt.

        Parameters:
        - password: Password to hash.
        - local_salt: Local salt.

        Returns:
        - str: Hashed password.
        """
        ...

    @abstractmethod
    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
        local_salt: str
    ) -> bool:
        """
        Verifies a password against the stored bcrypt hash.

        Parameters:
        - plain_password: Password to verify.
        - hashed_password: Hashed password.
        - local_salt: Local salt.

        Returns:
        - bool: True if password matches stored bcrypt hash.
        """
        ...
