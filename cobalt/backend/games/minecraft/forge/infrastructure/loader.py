#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timezone, timedelta
from typing import List, Optional

from domain.exceptions import UnexpectedError
from application.contracts.games import (
    AbstractLoader,
    AbstractServersService
)
from application.contracts.loggers import AbstractLogger
from infrastructure.mixins import HttpClientMixin


class ForgeLoader(AbstractLoader, HttpClientMixin):
    """
    Minecraft Forge loader.
    """
    FORGE_API: str = "https://files.minecraftforge.net/net/minecraftforge/forge/maven-metadata.json"
    DOWNLOAD_LINK: str = "https://maven.minecraftforge.net/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
    CACHE_TTL: int = 6 * 60 * 60

    _cached_mc_version: Optional[str]
    _cached_forge_version: Optional[str]
    _cached_updated_at: Optional[datetime]

    def __init__(
        self,
        game_id: int,
        name: str,
        logger: AbstractLogger,
        servers_service: AbstractServersService,
        timeout: float = 60.0
    ):
        AbstractLoader.__init__(
            self,
            game_id=game_id,
            name=name,
            servers_service=servers_service
        )

        HttpClientMixin.__init__(
            self,
            logger=logger,
            timeout=timeout
        )

        self._cached_mc_version = None
        self._cached_forge_version = None
        self._cache_updated_at = None

    def _is_cache_valid(
        self,
        version: str
    ) -> bool:
        """
        Checks whether the cached Forge version is still valid for the given Minecraft version.

        Parameters:
        - version: Minecraft version to check.

        Returns:
        - bool: True if cache is valid, False otherwise.
        """
        if not self._cache_updated_at or self._cached_mc_version != version:
            return False

        return (datetime.now(timezone.utc) - self._cache_updated_at) < timedelta(seconds=self.CACHE_TTL)

    def get_unsupported_versions(self) -> List[str]:
        """
        Returns the list of unsupported versions.

        Parameters:
        - None.

        Returns:
        - List: List of unsupported versions.
        """
        return [
            "1.7.10_pre4",
            "1.5.2",
            "1.5.1",
            "1.5",
            "1.4.7",
            "1.4.6",
            "1.4.5",
            "1.4.4",
            "1.4.3",
            "1.4.2",
            "1.4.1",
            "1.4.0",
            "1.3.2",
            "1.2.5",
            "1.2.4",
            "1.2.3",
            "1.1"
        ]

    def get_default_versions(self) -> List[str]:
        """
        Gets the default versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        return [
            "26.1.2",
            "26.1.1",
            "26.1",
            "1.21.11",
            "1.21.10",
            "1.21.9",
            "1.21.8",
            "1.21.7",
            "1.21.6",
            "1.21.5",
            "1.21.4",
            "1.21.3",
            "1.21.1",
            "1.21",
            "1.20.6",
            "1.20.4",
            "1.20.3",
            "1.20.2",
            "1.20.1",
            "1.20",
            "1.19.4",
            "1.19.3",
            "1.19.2",
            "1.19.1",
            "1.19",
            "1.18.2",
            "1.18.1",
            "1.18",
            "1.17.1",
            "1.16.5",
            "1.16.4",
            "1.16.3",
            "1.16.2",
            "1.16.1",
            "1.15.2",
            "1.15.1",
            "1.15",
            "1.14.4",
            "1.14.3",
            "1.14.2",
            "1.13.2",
            "1.12.2",
            "1.12.1",
            "1.12",
            "1.11.2",
            "1.11",
            "1.10.2",
            "1.10",
            "1.9.4",
            "1.9",
            "1.8.9",
            "1.8.8",
            "1.8",
            "1.7.10",
            "1.7.2",
            "1.6.4",
            "1.6.3",
            "1.6.2",
            "1.6.1"
        ]

    async def _fetch_forge_version(
        self,
        version: str
    ) -> Optional[str]:
        """
        Fetches the latest Forge version for the given Minecraft version.

        Parameters:
        - version: Minecraft version.

        Returns:
        - str: Full Forge version string or None on failure.
        """
        try:
            response = await self.request(
                url=self.FORGE_API,
                method="GET",
            )

            if not response or not isinstance(response, dict):
                return None

            forge_versions = response.get(version)

            if not forge_versions:
                return None

            return forge_versions[-1]

        except Exception:
            self.logger.exception(f'Error while getting "{self.name}" Forge version for "{version}":')

        return None

    async def _ensure_forge_version(
        self,
        version: str
    ) -> Optional[str]:
        """
        Fetches and caches the latest Forge version for the given Minecraft version.
        Invalidates cache if Minecraft version changed or TTL expired.

        Parameters:
        - version: Minecraft version.

        Returns:
        - str: Full Forge version string or None on failure.
        """
        if self._is_cache_valid(version):
            return self._cached_forge_version

        forge_version = await self._fetch_forge_version(version)

        if forge_version:
            self._cached_mc_version = version
            self._cached_forge_version = forge_version
            self._cache_updated_at = datetime.now(timezone.utc)

        return forge_version

    async def get_versions(self) -> List[str]:
        """
        Gets all available versions.

        Parameters:
        - None.

        Returns:
        - List: List of available versions.
        """
        try:
            response = await self.request(
                url=self.FORGE_API,
                method="GET",
            )

            if not response or not isinstance(response, dict):
                return self.get_default_versions()

            unsupported_versions = self.get_unsupported_versions()

            versions = [
                version for version in reversed(list(response.keys()))
                if version not in unsupported_versions
            ]

            return versions if versions else self.get_default_versions()

        except Exception:
            self.logger.exception(f'Error while getting "{self.name}" versions:')

        return self.get_default_versions()

    async def get_download_link(
        self,
        version: str
    ) -> str:
        """
        Gets a link for download.

        Parameters:
        - version: Game version.

        Returns:
        - str: Download URL.
        """
        forge_version = await self._ensure_forge_version(
            version=version
        )

        if not forge_version:
            self.logger.error(f'Failed to resolve Forge version for "{self.name}"')
            raise UnexpectedError("Could not fetch Forge version")

        return self.DOWNLOAD_LINK.format(
            version=forge_version
        )