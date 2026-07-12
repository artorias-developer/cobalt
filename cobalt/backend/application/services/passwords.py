#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import urandom
from hashlib import sha256

from bcrypt import hashpw, gensalt, checkpw

from application.contracts.services import AbstractPasswordsService
from application.contracts.loggers import AbstractLogger


class PasswordsService(AbstractPasswordsService):
    """
    Passwords service.
    """
    logger: AbstractLogger
    pepper: str
    bcrypt_rounds: int

    def __init__(
        self,
        logger: AbstractLogger,
        pepper: str,
        bcrypt_rounds: int = 12
    ):
        self.logger = logger
        self.pepper = pepper
        self.bcrypt_rounds = bcrypt_rounds

    def _prepare_password(
        self,
        password: str,
        salt: str
    ) -> bytes:
        """
        Prepares a password for hashing or verification.

        Parameters:
        - password: Password to prepare.
        - salt: User local salt.

        Returns:
        - bytes: SHA256 hash of the password with pepper and salt.
        """
        peppered_password = f"{password}{self.pepper}".encode("utf-8")
        peppered_hash = sha256(peppered_password).hexdigest()

        salted_hash = f"{salt}{peppered_hash}".encode("utf-8")
        return sha256(salted_hash).hexdigest().encode("utf-8")

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
        return urandom(length).hex()

    def hash_password(
        self,
        password: str,
        salt: str
    ) -> str:
        """
        Hashes a password using salt + pepper + SHA256 + bcrypt.

        Parameters:
        - password: Password to hash.
        - salt: User local salt.

        Returns:
        - str: Hashed password.
        """
        sha256_hash = self._prepare_password(
            password=password,
            salt=salt
        )

        bcrypt_hash = hashpw(
            sha256_hash,
            gensalt(self.bcrypt_rounds)
        )

        return bcrypt_hash.decode("utf-8")

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
        salt: str
    ) -> bool:
        """
        Verifies a password against the stored bcrypt hash.

        Parameters:
        - plain_password: Password to verify.
        - hashed_password: Hashed password.
        - salt: User local salt.

        Returns:
        - bool: True if password matches stored bcrypt hash.
        """
        sha256_hash = self._prepare_password(
            password=plain_password,
            salt=salt
        )

        return checkpw(
            sha256_hash,
            hashed_password.encode("utf-8")
        )
