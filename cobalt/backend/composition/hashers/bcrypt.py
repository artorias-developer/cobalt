#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.hashers import AbstractHasher
from application.contracts.loggers import AbstractLogger
from infrastructure.hashers import BcryptHasher
from infrastructure.configs import ApplicationConfig


def create_bcrypt_hasher(
    config: ApplicationConfig,
    logger: AbstractLogger
) -> AbstractHasher:
    """
    Creates the Bcrypt hasher.

    Parameters:
    - config: ApplicationConfig object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractHasher: AbstractHasher object.
    """
    return BcryptHasher(
        logger=logger,
        pepper=config.security.pepper,
        bcrypt_rounds=config.security.bcrypt_rounds
    )
