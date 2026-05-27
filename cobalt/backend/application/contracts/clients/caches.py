#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, Optional, Union, Iterable


class AbstractCachesClient(ABC):
    """
    Abstract caches client.
    """

    @abstractmethod
    def format_pattern(
        self,
        pattern: str,
        **kwargs: Any
    ) -> str:
        """
        Prepares key for specific format.

        Parameters:
        - pattern: Pattern template string.
        - **kwargs: Keyword arguments.

        Returns:
        - str: Formatted string.
        """
        ...

    @abstractmethod
    async def get(
        self,
        key: Optional[str] = None,
        pattern: Optional[str] = None,
        raise_on_error: bool = False
    ) -> Optional[Any]:
        """
        Gets a cached value by key or pattern.

        Parameters:
        - key: The cache key to get.
        - pattern: The cache key pattern (e.g., "users:item:*:john:*").
        - raise_on_error: If True, raises error instead of returning None on client errors.

        Returns:
        - Any: The cached value, or None if not found.
        """
        ...

    @abstractmethod
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None,
        raise_on_error: bool = False
    ) -> bool:
        """
        Sets a value in the cache.

        Parameters:
        - key: The key of the value.
        - value: The value to store.
        - expire: Optional expiration time in seconds.
        - raise_on_error: If True, raises error instead of returning False on client errors.

        Returns:
        - bool: True if the value was successfully set, False on error (when raise_on_error=False).
        """
        ...

    @abstractmethod
    async def expire(
        self,
        key: str,
        seconds: int,
        raise_on_error: bool = False
    ) -> None:
        """
        Sets a new TTL (expiration time) for a key.

        Parameters:
        - key: The cache key.
        - seconds: Expiration time in seconds.
        - raise_on_error: If True, raises error instead of returning None on client errors.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def delete(
        self,
        keys: Optional[Union[str, Iterable[str]]] = None,
        patterns: Optional[Union[str, Iterable[str]]] = None,
        batch_size: int = 500,
        raise_on_error: bool = False
    ) -> None:
        """
        Deletes cached values by keys and/or patterns.

        Parameters:
        - keys: A single key or an iterable of keys to delete directly.
        - patterns: A single pattern or an iterable of patterns to delete by match.
        - batch_size: Number of keys to delete at once when deleting by pattern.
        - raise_on_error: If True, raises error instead of returning None on client errors.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def clear(
        self,
        raise_on_error: bool = False
    ) -> None:
        """
        Clears all cached values.

        Parameters:
        - raise_on_error: If True, raises error instead of returning None on client errors.

        Returns:
        - None.
        """
        ...