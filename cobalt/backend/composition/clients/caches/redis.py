#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from redis.asyncio import Redis

from application.contracts.clients import AbstractCachesClient
from application.contracts.loggers import AbstractLogger
from infrastructure.clients.caches.redis import RedisClient
from infrastructure.configs import ApplicationConfig


def create_redis_client(
    config: ApplicationConfig,
    logger: AbstractLogger
) -> AbstractCachesClient:
    """
    Creates a Redis client.

    Parameters:
    - config: ApplicationConfig object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractCachesClient: AbstractCachesClient object.
    """
    base_client = Redis.from_url(
        url=config.redis.url
    )

    return RedisClient(
        logger=logger,
        redis_client=base_client
    )
