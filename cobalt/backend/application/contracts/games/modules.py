#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, TYPE_CHECKING

from domain.exceptions import NotFoundError
from application.contracts.games import AbstractLoader
from application.dtos import (
    GameDto,
    GameCreateDto,
    LoaderDto,
    LoaderCreateDto,
    LoaderUpdateDto
)
if TYPE_CHECKING:
    from composition import ApplicationContainer


class AbstractGameModule(ABC):
    """
    Abstract game module.
    """
    UPDATE_THRESHOLD_HOURS: int = 24
    loaders: Dict[str, AbstractLoader]

    game_id: int
    name: str
    has_logs_timestamp: bool
    app_containers_dir: Path
    host_containers_dir: Path
    dependencies: "ApplicationContainer"

    def __init__(
        self,
        name: str,
        has_logs_timestamp: bool,
        app_containers_dir: Path,
        host_containers_dir: Path,
        dependencies: "ApplicationContainer"
    ):
        self.name = name
        self.has_logs_timestamp = has_logs_timestamp
        self.app_containers_dir = app_containers_dir
        self.host_containers_dir = host_containers_dir
        self.dependencies = dependencies

        self.loaders = {}

    async def _create_game(self) -> GameDto:
        """
        Creates a new game.

        Parameters:
        - None.

        Returns:
        - GamesCreateDto: GamesCreateDto object.
        """
        create_dto = GameCreateDto(
            name=self.name
        )

        game = await self.dependencies.services.games.create_one(
            dto=create_dto
        )

        return game

    def _should_update_loader(
        self,
        existing_loader: LoaderDto
    ) -> bool:
        """
        Checks if loader should be updated based on last update time.

        Parameters:
        - existing_loader: LoaderDto object.

        Returns:
        - bool: True if loader should be updated, False otherwise.
        """
        time_since_update = datetime.now(timezone.utc) - existing_loader.updated_at
        threshold = timedelta(hours=self.UPDATE_THRESHOLD_HOURS)

        if time_since_update < threshold:
            return False

        return True

    async def _create_loader(
        self,
        loader: AbstractLoader
    ) -> LoaderDto:
        """
        Creates a new loader.

        Parameters:
        - loader: Loader instance.

        Returns:
        - LoaderDto: LoaderDto object.
        """
        versions = await loader.get_versions()

        request_dto = LoaderCreateDto(
            name=loader.name,
            versions=versions
        )

        created_loader = await self.dependencies.services.loaders.create_one(
            game_id=loader.game_id,
            dto=request_dto
        )

        return created_loader

    async def _update_loader(
        self,
        loader: AbstractLoader,
        existing_loader: LoaderDto
    ) -> None:
        """
        Updates an existing loader if update threshold is met.

        Parameters:
        - loader: Loader instance.
        - existing_loader: LoaderDto object.

        Returns:
        - None.
        """
        if not self._should_update_loader(existing_loader):
            return

        versions = await loader.get_versions()

        if len(existing_loader.versions) > len(versions):
            versions = existing_loader.versions

        request_dto = LoaderUpdateDto(
            id=existing_loader.id,
            versions=versions
        )

        await self.dependencies.services.loaders.update_one(
            game_id=existing_loader.game_id,
            dto=request_dto
        )

    async def update_loaders(self) -> None:
        """
        Checks all registered loaders and updates their versions if the update threshold has been reached.

        Parameters:
        - None.

        Returns:
        - None.
        """
        for _, loader in self.loaders.items():
            try:
                existing_loader = await self.dependencies.services.loaders.get_one_by_name(
                    game_id=loader.game_id,
                    name=loader.name
                )

                await self._update_loader(
                    loader=loader,
                    existing_loader=existing_loader
                )
            except Exception:
                self.dependencies.logger.exception(f'Error while updating loader "{loader.name}" for "{self.name}":')

    async def setup_game(self) -> None:
        """
        Setups game module game.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            game = await self.dependencies.services.games.get_one_by_name(
                name=self.name
            )
        except NotFoundError:
            game = await self._create_game()

        self.game_id = game.id

    async def setup_loaders(self) -> None:
        """
        Setups game module loaders.

        Parameters:
        - None.

        Returns:
        - None.
        """
        loaders = self.get_loaders()

        for loader in loaders:
            try:
                game_loader = await self.dependencies.services.loaders.get_one_by_name(
                    game_id=self.game_id,
                    name=loader.name
                )

                await self._update_loader(
                    loader=loader,
                    existing_loader=game_loader
                )
            except NotFoundError:
                game_loader = await self._create_loader(
                    loader=loader
                )
            except Exception:
                self.dependencies.logger.exception(f'Error while setup loader "{loader.name}" for "{self.name}":')

                continue

            self.loaders[game_loader.name] = loader

    async def setup(self) -> None:
        """
        Setups game module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        await self.setup_game()
        await self.setup_loaders()

    @abstractmethod
    def get_loaders(self) -> List:
        """
        Gets list of loaders for the game module.

        Parameters:
        - None.

        Returns:
        - List: List of loader instances.
        """
        ...
