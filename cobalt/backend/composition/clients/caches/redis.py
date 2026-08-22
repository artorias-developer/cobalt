#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from redis.asyncio import Redis

from application.contracts.clients import AbstractCacheClient
from application.contracts.loggers import AbstractLogger
from infrastructure.clients.caches.redis import RedisClient
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
    base_client = Redis.from_url(
        url=config.redis.url
    )

    return RedisClient(
        logger=logger,
        redis_client=base_client
    )
