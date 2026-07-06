#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from redis.asyncio import Redis

from application.contracts.managers import AbstractI18nManager
from application.contracts.clients import AbstractCachesClient
from application.contracts.loggers import AbstractLogger
from infrastructure.clients.caches.redis import RedisClient
from infrastructure.configs import ApplicationConfig


def create_redis_client(
    config: ApplicationConfig,
    i18n_manager: AbstractI18nManager,
    logger: AbstractLogger
) -> AbstractCachesClient:
    """
    Creates a Redis client.

    Parameters:
    - config: ApplicationConfig object.
    - i18n_manager: AbstractI18nManager object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractCachesClient: AbstractCachesClient object.
    """
    base_client = Redis.from_url(
        url=config.redis.url
    )

    return RedisClient(
        logger=logger,
        redis_client=base_client,
        i18n_manager=i18n_manager
    )
