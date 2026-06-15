#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path
from typing import List

from application.contracts.games import AbstractGameModule
from composition import ApplicationContainer
from games.minecraft.fabric.application.services import FabricServersService
from games.minecraft.forge.application.services import ForgeServersService
from games.minecraft.paper.application.services import PaperServersService
from games.minecraft.fabric.infrastructure import FabricLoader
from games.minecraft.forge.infrastructure import ForgeLoader
from games.minecraft.paper.infrastructure import PaperLoader


class MinecraftGameModule(AbstractGameModule):
    """
    Minecraft game module.
    """
    game_module_root_dir: Path

    def __init__(
        self,
        app_containers_dir: Path,
        host_containers_dir: Path,
        dependencies: ApplicationContainer
    ):
        super().__init__(
            name="minecraft",
            has_logs_timestamp=True,
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
        fabric_build_dir = self.game_module_root_dir / "fabric" / "build"
        forge_build_dir = self.game_module_root_dir / "forge" / "build"
        paper_build_dir = self.game_module_root_dir / "paper" / "build"

        fabric_servers_service = FabricServersService(
            build_dir=fabric_build_dir,
            app_containers_dir=self.app_containers_dir,
            host_containers_dir=self.host_containers_dir,
            core_servers_service=self.dependencies.services.servers,
            containers_client=self.dependencies.clients.containers,
            connections_manager=self.dependencies.managers.connections,
            logger=self.dependencies.logger
        )

        forge_servers_service = ForgeServersService(
            build_dir=forge_build_dir,
            app_containers_dir=self.app_containers_dir,
            host_containers_dir=self.host_containers_dir,
            core_servers_service=self.dependencies.services.servers,
            containers_client=self.dependencies.clients.containers,
            connections_manager=self.dependencies.managers.connections,
            logger=self.dependencies.logger
        )

        paper_servers_service = PaperServersService(
            build_dir=paper_build_dir,
            app_containers_dir=self.app_containers_dir,
            host_containers_dir=self.host_containers_dir,
            core_servers_service=self.dependencies.services.servers,
            containers_client=self.dependencies.clients.containers,
            connections_manager=self.dependencies.managers.connections,
            logger=self.dependencies.logger
        )

        return [
            FabricLoader(
                game_id=self.game_id,
                name="fabric",
                servers_service=fabric_servers_service,
                logger=self.dependencies.logger
            ),
            ForgeLoader(
                game_id=self.game_id,
                name="forge",
                servers_service=forge_servers_service,
                logger=self.dependencies.logger
            ),
            PaperLoader(
                game_id=self.game_id,
                name="paper",
                servers_service=paper_servers_service,
                logger=self.dependencies.logger
            )
        ]
