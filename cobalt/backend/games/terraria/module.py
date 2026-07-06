#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path
from typing import List

from application.contracts.games import AbstractGameModule
from composition import ApplicationContainer
from games.terraria.vanilla.application.services import VanillaServersService
from games.terraria.tmodloader.application.services import TModLoaderServersService
from games.terraria.vanilla.infrastructure import VanillaLoader
from games.terraria.tmodloader.infrastructure import TModLoaderLoader


class TerrariaGameModule(AbstractGameModule):
    """
    Terraria game module.
    """
    game_module_root_dir: Path

    def __init__(
        self,
        app_containers_dir: Path,
        host_containers_dir: Path,
        dependencies: ApplicationContainer
    ):
        super().__init__(
            name="terraria",
            has_logs_timestamp=False,
            app_containers_dir=app_containers_dir,
            host_containers_dir=host_containers_dir,
            dependencies=dependencies
        )

        self.game_module_root_dir = Path(__file__).parents[0]

    def get_loaders(self) -> List:
        """
        Gets list of loaders for the game module.

        Parameters:
        - None.

        Returns:
        - List: List of loader instances.
        """
        vanilla_build_dir = self.game_module_root_dir / "vanilla" / "build"
        tmodloader_build_dir = self.game_module_root_dir / "tmodloader" / "build"

        vanilla_servers_service = VanillaServersService(
            build_dir=vanilla_build_dir,
            app_containers_dir=self.app_containers_dir,
            host_containers_dir=self.host_containers_dir,
            core_servers_service=self.dependencies.services.servers,
            containers_client=self.dependencies.clients.containers,
            connections_manager=self.dependencies.managers.connections,
            logger=self.dependencies.logger
        )

        tmodloader_servers_service = TModLoaderServersService(
            build_dir=tmodloader_build_dir,
            app_containers_dir=self.app_containers_dir,
            host_containers_dir=self.host_containers_dir,
            core_servers_service=self.dependencies.services.servers,
            containers_client=self.dependencies.clients.containers,
            connections_manager=self.dependencies.managers.connections,
            logger=self.dependencies.logger
        )

        return [
            VanillaLoader(
                game_id=self.game_id,
                name="vanilla",
                servers_service=vanilla_servers_service,
                logger=self.dependencies.logger
            ),
            TModLoaderLoader(
                game_id=self.game_id,
                name="tmodloader",
                servers_service=tmodloader_servers_service,
                logger=self.dependencies.logger
            )
        ]
