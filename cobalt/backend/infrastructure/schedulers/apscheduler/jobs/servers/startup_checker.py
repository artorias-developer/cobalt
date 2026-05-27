#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from domain.exceptions import NotFoundError
from domain.enums import ServerStatusEnum
from application.contracts.services import AbstractServersService
from application.contracts.loggers import AbstractLogger
from application.dtos import (
    ServersGetPageDto,
    ServerUpdateDto
)
from infrastructure.schedulers.apscheduler.jobs import BaseApschedulerJob


class StartupServersCheckerJob(BaseApschedulerJob):
    """
    Job for checking failed servers on startup.
    """
    servers_service: AbstractServersService

    def __init__(
        self,
        servers_service: AbstractServersService,
        logger: AbstractLogger
    ):
        super().__init__(logger)

        self.servers_service = servers_service

    async def execute(self) -> None:
        """
        Changes the status of servers to FAILED if the container was not created.

        Parameters:
        - None.

        Returns:
        - None.
        """
        current_page = 1
        total_pages = 1
        all_servers = []

        while current_page <= total_pages:
            request_dto = ServersGetPageDto(
                page=current_page,
                limit=100
            )

            try:
                page = await self.servers_service.get_page(
                    dto=request_dto
                )
            except NotFoundError:
                break

            all_servers.extend(page.servers)
            total_pages = page.pages
            current_page += 1

        for server in all_servers:
            if server.status not in [
                ServerStatusEnum.PENDING,
                ServerStatusEnum.PROCESSING
            ]:
                continue

            update_dto = ServerUpdateDto(
                status=ServerStatusEnum.FAILED
            )

            await self.servers_service.update_one(
                server_id=server.id,
                dto=update_dto
            )
