#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from contextlib import asynccontextmanager
from argparse import ArgumentParser
from typing import AsyncGenerator, Any, Dict

from fastapi import FastAPI, APIRouter
from uvicorn import run as uvicorn_run

from application.contracts.games import AbstractGameModule
from infrastructure.databases.postgres import check_default_user
from infrastructure.configs import (
    ApplicationConfig,
    get_application_config
)
from games import ENABLED_GAME_MODULES
from composition import (
    ApplicationContainer,
    create_fastapi_ioc_container
)


class CobaltApplication:
    """
    Cobalt application.
    """
    app: FastAPI
    router: APIRouter
    config: ApplicationConfig
    dependencies: ApplicationContainer
    game_modules: Dict[str, AbstractGameModule]

    def __init__(self):
        self.game_modules = {}

    async def _initialize_dependencies(self) -> None:
        """
        Initializes the dependencies.

        Parameters:
        - None.

        Returns:
        - None.
        """
        await self.dependencies.clients.containers.initialize()
        await self.dependencies.queue.initialize()

    async def _destroy_dependencies(self) -> None:
        """
        Destroys the dependencies.

        Parameters:
        - None.

        Returns:
        - None.
        """
        await self.dependencies.clients.containers.close()

    async def _initialize_game_modules(self) -> None:
        """
        Initializes the game modules.

        Parameters:
        - None.

        Returns:
        - None.
        """
        app_containers_dir = self.config.server.app_containers_dir
        app_containers_dir.mkdir(exist_ok=True)

        for game_module in ENABLED_GAME_MODULES:
            module: AbstractGameModule = game_module(
                dependencies=self.dependencies,
                app_containers_dir=app_containers_dir,
                host_containers_dir=self.config.server.host_containers_dir
            )

            await module.setup()

            self.game_modules[module.name] = module

    async def _check_default_user(self) -> None:
        """
        Creates an admin user if there is no admin in the database.

        Parameters:
        - None.

        Returns:
        - None.
        """
        await check_default_user(
            roles_service=self.dependencies.services.roles,
            users_service=self.dependencies.services.users,
            logger=self.dependencies.logger
        )

    def _enable_cron_jobs(self) -> None:
        """
        Enables all scheduler cron jobs.

        Parameters:
        - None.

        Returns:
        - None.
        """
        scheduler = self.dependencies.scheduler

        for job in self.dependencies.jobs:
            scheduler.add_job(
                name=job.name,
                job=job.instance,
                trigger=job.trigger
            )

        scheduler.start()

    def _disable_cron_jobs(self) -> None:
        """
        Disables all scheduler cron jobs.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self.dependencies.scheduler.shutdown(
            wait=False
        )

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncGenerator[None, Any]:
        """
        FastAPI app lifespan function.

        Parameters:
        - app: Application object.

        Returns:
        - None.
        """
        await self._initialize_dependencies()
        await self._initialize_game_modules()
        await self._check_default_user()
        self._enable_cron_jobs()
        self.dependencies.logger.info(f"Cobalt running on http://{self.config.server.host}:{self.config.server.port}")
        yield
        self._disable_cron_jobs()
        await self._destroy_dependencies()

    def initialize(self) -> None:
        """
        Initializes the application.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self.config = get_application_config()
        self.router = APIRouter(prefix="/api/v1")
        self.app = FastAPI(
            lifespan=self.lifespan,
            title="Cobalt API",
            version="1.0.0"
        )

        self.dependencies = create_fastapi_ioc_container(
            app=self.app,
            router=self.router,
            config=self.config,
            game_modules=self.game_modules
        )

        self.app.include_router(self.router)

    def run(self) -> None:
        """
        Runs the application.

        Parameters:
        - None.

        Returns:
        - None.
        """
        parser = ArgumentParser(
            description="Cobalt server startup parameters."
        )

        parser.add_argument(
            "--host",
            type=str,
            default=self.config.server.host,
            help="Host to bind to."
        )

        parser.add_argument(
            "--port",
            type=int,
            default=self.config.server.port,
            help="Port to bind to."
        )

        args = parser.parse_args()

        uvicorn_run(
            app=self.app,
            host=args.host,
            port=args.port,
            workers=1,
            log_config=None,
            access_log=False
        )

def main() -> None:
    """
    Run the Cobalt application.

    Parameters:
    - None.

    Returns:
    - None.
    """
    application = CobaltApplication()
    application.initialize()
    application.run()

if __name__ == "__main__":
    main()