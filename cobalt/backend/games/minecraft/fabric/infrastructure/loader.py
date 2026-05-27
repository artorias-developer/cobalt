#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
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


class FabricLoader(AbstractLoader, HttpClientMixin):
    """
    Minecraft Fabric loader.
    """
    FABRIC_META_API: str = "https://meta.fabricmc.net/v2"
    DOWNLOAD_LINK: str = "https://meta.fabricmc.net/v2/versions/loader/{game_version}/{loader_version}/{installer_version}/server/jar"
    CACHE_TTL: int = 6 * 60 * 60

    _loader_version: Optional[str]
    _installer_version: Optional[str]
    _cache_updated_at: Optional[datetime]

    def __init__(
        self,
        game_id: int,
        name: str,
        logger: AbstractLogger,
        servers_service: AbstractServersService,
        timeout: Optional[float] = 60.0
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

        self._loader_version = None
        self._installer_version = None
        self._cache_updated_at = None

    def _is_cache_valid(self) -> bool:
        """
        Checks whether the cached versions are still valid.

        Parameters:
        - None.

        Returns:
        - bool: True if cache is valid, False otherwise.
        """
        if not self._cache_updated_at:
            return False

        return (datetime.now(timezone.utc) - self._cache_updated_at) < timedelta(seconds=self.CACHE_TTL)

    @staticmethod
    def get_unsupported_versions() -> List[str]:
        """
        Returns the list of unsupported versions.

        Parameters:
        - None.

        Returns:
        - List: List of unsupported versions.
        """
        return []

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
            "1.21.2",
            "1.21.1",
            "1.21",
            "1.20.6",
            "1.20.5",
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
            "1.17",
            "1.16.5",
            "1.16.4",
            "1.16.3",
            "1.16.2",
            "1.16.1",
            "1.16",
            "1.15.2",
            "1.15.1",
            "1.15",
            "1.14.4",
            "1.14.3",
            "1.14.2",
            "1.14.1",
            "1.14"
        ]

    async def _fetch_latest_loader_version(self) -> Optional[str]:
        """
        Fetches the latest stable Fabric loader version.

        Parameters:
        - None.

        Returns:
        - str: Latest loader version or None on failure.
        """
        try:
            response = await self.request(
                url=f"{self.FABRIC_META_API}/versions/loader",
                method="GET",
            )

            if not response or not isinstance(response, list):
                return None

            for entry in response:
                version = entry.get("version")
                if version:
                    return version

        except Exception:
            self.logger.exception(f'Error while getting "{self.name}" loader version:')

        return None

    async def _fetch_latest_installer_version(self) -> Optional[str]:
        """
        Fetches the latest stable Fabric installer version.

        Parameters:
        - None.

        Returns:
        - str: Latest installer version or None on failure.
        """
        try:
            response = await self.request(
                url=f"{self.FABRIC_META_API}/versions/installer",
                method="GET",
            )

            if not response or not isinstance(response, list):
                return None

            for entry in response:
                version = entry.get("version")
                if version:
                    return version

        except Exception:
            self.logger.exception(f'Error while getting "{self.name}" installer version:')

        return None

    async def _ensure_meta_versions(self) -> bool:
        """
        Fetches and caches loader and installer versions if cache is missing or expired.

        Parameters:
        - None.

        Returns:
        - bool: True if both versions are available, False otherwise.
        """
        if self._is_cache_valid():
            return bool(self._loader_version and self._installer_version)

        self._loader_version = await self._fetch_latest_loader_version()
        self._installer_version = await self._fetch_latest_installer_version()

        if self._loader_version and self._installer_version:
            self._cache_updated_at = datetime.now(timezone.utc)

        return bool(self._loader_version and self._installer_version)

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
                url=f"{self.FABRIC_META_API}/versions/game",
                method="GET",
            )

            if not response or not isinstance(response, list):
                return self.get_default_versions()

            unsupported_versions = self.get_unsupported_versions()

            versions = [
                entry["version"]
                for entry in response
                if entry.get("version")
                and entry.get("stable", False)
                and entry["version"] not in unsupported_versions
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
        if not await self._ensure_meta_versions():
            self.logger.error(f'Failed to resolve loader/installer versions for "{self.name}"')
            raise UnexpectedError("Could not fetch Fabric loader or installer version")

        return self.DOWNLOAD_LINK.format(
            game_version=version,
            loader_version=self._loader_version,
            installer_version=self._installer_version,
        )