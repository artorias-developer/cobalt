#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timezone, timedelta

from domain.exceptions import NotFoundError
from domain.enums import ServerStateEnum
from application.contracts.services import AbstractServersService
from application.contracts.loggers import AbstractLogger
from application.dtos import (
    ServersGetPageDto,
    ServerUpdateDto
)
from infrastructure.schedulers.apscheduler.jobs import BaseApschedulerJob


class FailedServersCheckerJob(BaseApschedulerJob):
    """
    Job for checking failed servers.
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
        Changes the state of servers to FAILED if the container was not created.

        Parameters:
        - None.

        Returns:
        - None.
        """
        current_page = 1
        total_pages = 1
        all_servers = []

        while current_page <= total_pages:
            page_dto = ServersGetPageDto(
                page=current_page,
                limit=100
            )

            try:
                page = await self.servers_service.get_page(
                    dto=page_dto
                )
            except NotFoundError:
                break

            all_servers.extend(page.servers)
            total_pages = page.pages
            current_page += 1

        now = datetime.now(timezone.utc)

        for server in all_servers:
            if server.state not in [
                ServerStateEnum.PENDING,
                ServerStateEnum.PROCESSING
            ]:
                continue

            if now - server.updated_at <= timedelta(hours=3):
                continue

            update_dto = ServerUpdateDto(
                state=ServerStateEnum.FAILED
            )

            await self.servers_service.update_one(
                server_id=server.id,
                dto=update_dto
            )
