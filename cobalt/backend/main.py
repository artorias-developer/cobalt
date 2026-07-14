#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from contextlib import asynccontextmanager
from argparse import ArgumentParser
from typing import AsyncGenerator, Any, Dict, List

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
    SchedulerJob,
    create_structlog_logger,
    create_bcrypt_hasher,
    create_apscheduler_scheduler,
    create_asyncio_queue,
    create_apscheduler_jobs,
    create_fastapi_managers_container,
    create_redis_prometheus_docker_clients_container,
    create_fastapi_postgres_mappers_container,
    create_postgres_database_container,
    create_services_container,
    setup_fastapi_interceptors,
    setup_fastapi_middlewares,
    setup_fastapi_routers
)


class CobaltApplication:
    """
    Cobalt application.
    """
    app: FastAPI
    router: APIRouter
    config: ApplicationConfig
    dependencies: ApplicationContainer
    jobs: List[SchedulerJob]
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

        for job in self.jobs:
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

        logger = create_structlog_logger(
            config=self.config
        )

        hasher = create_bcrypt_hasher(
            config=self.config,
            logger=logger
        )

        scheduler = create_apscheduler_scheduler(
            logger=logger
        )

        queue = create_asyncio_queue(
            logger=logger
        )

        managers_container = create_fastapi_managers_container(
            config=self.config,
            logger=logger
        )

        clients_container = create_redis_prometheus_docker_clients_container(
            config=self.config,
            managers=managers_container,
            logger=logger
        )

        mappers_container = create_fastapi_postgres_mappers_container()

        database_container = create_postgres_database_container(
            config=self.config,
            managers=managers_container,
            mappers=mappers_container,
            logger=logger
        )

        services_container = create_services_container(
            config=self.config,
            managers=managers_container,
            clients=clients_container,
            mappers=mappers_container,
            database=database_container,
            logger=logger,
            hasher=hasher,
            queue=queue,
            game_modules=self.game_modules
        )

        self.jobs = create_apscheduler_jobs(
            services=services_container,
            managers=managers_container,
            logger=logger,
            game_modules=self.game_modules
        )

        setup_fastapi_interceptors(
            managers=managers_container,
            logger=logger
        )

        setup_fastapi_middlewares(
            app=self.app,
            config=self.config,
            managers=managers_container,
            services=services_container,
            logger=logger
        )

        setup_fastapi_routers(
            router=self.router,
            managers=managers_container,
            mappers=mappers_container,
            services=services_container
        )

        self.dependencies = ApplicationContainer(
            logger=logger,
            hasher=hasher,
            scheduler=scheduler,
            queue=queue,
            clients=clients_container,
            managers=managers_container,
            mappers=mappers_container,
            services=services_container,
            database=database_container
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