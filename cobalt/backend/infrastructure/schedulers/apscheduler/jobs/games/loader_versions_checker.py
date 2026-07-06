#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict

from application.contracts.loggers import AbstractLogger
from application.contracts.games import AbstractGameModule
from infrastructure.schedulers.apscheduler.jobs import BaseApschedulerJob


class LoaderVersionsCheckerJob(BaseApschedulerJob):
    """
    Job for checking and updating loader versions.
    """
    game_modules: Dict[str, AbstractGameModule]

    def __init__(
        self,
        game_modules: Dict[str, AbstractGameModule],
        logger: AbstractLogger
    ):
        super().__init__(logger)

        self.game_modules = game_modules

    async def execute(self) -> None:
        """
        Sends last server RAM metrics to all subscribers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        for _, game_module in self.game_modules.items():
            await game_module.update_loaders()