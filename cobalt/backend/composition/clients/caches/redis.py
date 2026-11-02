#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.clients import AbstractCacheClient
from application.contracts.loggers import AbstractLogger
from infrastructure.clients import RedisClient
from infrastructure.configs import ApplicationConfig


def create_redis_client(
    config: ApplicationConfig,
    logger: AbstractLogger
) -> AbstractCacheClient:
    """
    Creates a Redis client.

    Parameters:
    - config: ApplicationConfig object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractCacheClient: AbstractCacheClient object.
    """
    return RedisClient(
        redis_url=config.redis.url,
        logger=logger
    )
