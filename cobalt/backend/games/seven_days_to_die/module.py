#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path
from typing import List

from application.contracts.games import AbstractGameModule
from composition import ApplicationContainer
from games.seven_days_to_die.vanilla.application.services import VanillaServersService
from games.seven_days_to_die.vanilla.infrastructure import VanillaLoader


class SevenDaysToDieGameModule(AbstractGameModule):
    """
    7 Days to Die game module.
    """
    game_module_root_dir: Path

    def __init__(
        self,
        container: ApplicationContainer,
        app_containers_dir: Path,
        host_containers_dir: Path
    ):
        super().__init__(
            name="seven_days_to_die",
            has_logs_timestamp=False,
            app_containers_dir=app_containers_dir,
            host_containers_dir=host_containers_dir,
            container=container
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

        vanilla_servers_service = VanillaServersService(
            build_dir=vanilla_build_dir,
            app_containers_dir=self.app_containers_dir,
            host_containers_dir=self.host_containers_dir,
            core_servers_service=self.container.services.servers,
            containers_client=self.container.clients.containers,
            connections_manager=self.container.managers.connections,
            logger=self.container.logger
        )

        return [
            VanillaLoader(
                game_id=self.game_id,
                name="vanilla",
                servers_service=vanilla_servers_service,
                logger=self.container.logger
            )
        ]