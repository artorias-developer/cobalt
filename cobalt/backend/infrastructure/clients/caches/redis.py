#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from collections import defaultdict
from typing import Optional, Any, Union, Iterable

from redis.asyncio import Redis

from domain.exceptions import UnexpectedError
from application.contracts.clients import AbstractCacheClient
from application.contracts.loggers import AbstractLogger


class RedisClient(AbstractCacheClient):
    """
    Redis client.
    """
    _redis_client: Optional[Redis]

    logger: AbstractLogger
    redis_url: str

    def __init__(
        self,
        logger: AbstractLogger,
        redis_url: str
    ):
        self.logger = logger
        self.redis_url = redis_url

        self._redis_client = None

    async def initialize(self) -> None:
        """
        Create the Redis client from the URL, check the connection and prepare the client for use. Should be
        called on application startup if the client isn't used as an async context manager.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if self._redis_client is not None:
            return

        client = Redis.from_url(url=self.redis_url)

        try:
            await client.ping()
        except Exception:
            await client.aclose()
            raise

        self._redis_client = client

    async def close(self) -> None:
        """
        Close the connection to Redis and free its connection pool. Should be called on application shutdown
        if the client wasn't used as an async context manager.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if self._redis_client is not None:
            await self._redis_client.aclose()
            self._redis_client = None

    def format_pattern(
        self,
        pattern: str,
        **kwargs: Any
    ) -> str:
        """
        Prepares key for specific format.

        Parameters:
        - key: Key template string.
        - **kwargs: Keyword arguments.

        Returns:
        - str: Formatted string.
        """
        return pattern.format_map(
            defaultdict(lambda: "*", **kwargs)
        )

    async def get(
        self,
        key: Optional[str] = None,
        pattern: Optional[str] = None,
        raise_on_error: bool = False
    ) -> Optional[Any]:
        """
        Gets a cached value from Redis by key or pattern.

        Parameters:
        - key: The Redis key to get.
        - pattern: The Redis key pattern (e.g., "users:item:*:john:*").
        - raise_on_error: If True, raises UnexpectedError instead of returning None on Redis errors.

        Returns:
        - Any: The cached value, or None if not found or on error (when raise_on_error=False).
        """
        try:
            if key:
                cached = await self._redis_client.get(key)
                return cached if cached else None

            if pattern:
                async for pattern_key in self._redis_client.scan_iter(match=pattern):
                    cached = await self._redis_client.get(pattern_key)

                    if cached:
                        return cached

            return None

        except Exception as e:
            if raise_on_error:
                raise UnexpectedError("Error while getting value from cache") from e

            self.logger.exception(f"Error while getting key={key} or pattern={pattern} from Redis:")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None,
        raise_on_error: bool = False
    ) -> bool:
        """
        Sets a value to Redis.

        Parameters:
        - key: The key of the value.
        - value: The value to store.
        - expire: The expiration time in seconds.
        - raise_on_error: If True, raises UnexpectedError instead of returning False on Redis errors.

        Returns:
        - bool: True if the value was successfully set, False on error (when raise_on_error=False).
        """
        try:
            await self._redis_client.set(
                name=key,
                value=value,
                ex=expire
            )
            return True
        except Exception as e:
            if raise_on_error:
                raise UnexpectedError("Error while writing value to cache") from e

            self.logger.exception(f"Error while setting {key} in Redis:")
            return False

    async def expire(
        self,
        key: str,
        seconds: int,
        raise_on_error: bool = False
    ) -> None:
        """
        Sets a new TTL (expiration time) for a key.

        Parameters:
        - key: The Redis key.
        - seconds: Expiration time in seconds.
        - raise_on_error: If True, raises UnexpectedError instead of returning None on Redis errors.

        Returns:
        - None.
        """
        try:
            await self._redis_client.expire(key, seconds)
        except Exception as e:
            if raise_on_error:
                raise UnexpectedError("Error while setting expire in cache") from e

            self.logger.exception(f"Error while setting expire for {key}:")

    async def delete(
        self,
        keys: Optional[Union[str, Iterable[str]]] = None,
        patterns: Optional[Union[str, Iterable[str]]] = None,
        batch_size: int = 500,
        raise_on_error: bool = False
    ) -> None:
        """
        Deletes cached values from Redis by keys and/or patterns.

        Parameters:
        - keys: A single key or an iterable of keys to delete directly.
        - patterns: A single pattern or an iterable of patterns to delete by match.
        - batch_size: Number of keys to delete at once when deleting by pattern.
        - raise_on_error: If True, raises UnexpectedError instead of returning None on Redis errors.

        Returns:
        - None.
        """
        try:
            if isinstance(keys, str):
                keys = [keys]

            if isinstance(patterns, str):
                patterns = [patterns]

            if keys:
                await self._redis_client.delete(*keys)

            if patterns:
                for pattern in patterns:
                    batch = []

                    async for key in self._redis_client.scan_iter(match=pattern):
                        batch.append(key)

                        if len(batch) >= batch_size:
                            await self._redis_client.delete(*batch)
                            batch.clear()

                    if batch:
                        await self._redis_client.delete(*batch)

        except Exception as e:
            if raise_on_error:
                raise UnexpectedError("Error while deleting values from cache") from e

            self.logger.exception(f"Error while deleting keys={keys} or patterns={patterns} from Redis:")

    async def clear(
        self,
        raise_on_error: bool = False
    ) -> None:
        """
        Clears all cached values from Redis.

        Parameters:
        - raise_on_error: If True, raises UnexpectedError instead of returning None on Redis errors.

        Returns:
        - None.
        """
        try:
            await self._redis_client.flushdb()
        except Exception as e:
            if raise_on_error:
                raise UnexpectedError("Error while clearing cache") from e

            self.logger.exception(f"Error while clearing Redis cache:")