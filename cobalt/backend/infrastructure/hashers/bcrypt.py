#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import urandom
from hashlib import sha256

from bcrypt import hashpw, gensalt, checkpw

from application.contracts.hashers import AbstractHasher
from application.contracts.loggers import AbstractLogger


class BcryptHasher(AbstractHasher):
    """
    Bcrypt hasher.
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
        - salt: Secret salt.

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

    def hash(
        self,
        plain: str,
        salt: str
    ) -> str:
        """
        Hashes a plain text using salt + pepper + SHA256 + bcrypt.

        Parameters:
        - plain: Plain text to hash.
        - salt: Secret salt.

        Returns:
        - str: Hashed text.
        """
        sha256_hash = self._prepare_password(
            password=plain,
            salt=salt
        )

        bcrypt_hash = hashpw(
            sha256_hash,
            gensalt(self.bcrypt_rounds)
        )

        return bcrypt_hash.decode("utf-8")

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
        sha256_hash = self._prepare_password(
            password=plain,
            salt=salt
        )

        return checkpw(
            sha256_hash,
            hashed.encode("utf-8")
        )
