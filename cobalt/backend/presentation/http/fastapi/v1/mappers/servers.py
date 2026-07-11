#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.dtos import (
    ServerDto,
    ServersGetPageDto,
    ServersPageDto,
    ServerCreateDto,
    ServerUpdateDto,
    ServerUpgradeDto,
    ServerExecuteDto,
    ServerStatusDto
)
from presentation.contracts.http.mappers import (
    AbstractServersRouterMapper,
    AbstractAttributesRouterMapper,
    AbstractGamesRouterMapper,
    AbstractLoadersRouterMapper
)
from presentation.http.fastapi.v1.schemas import (
    ServerSchema,
    ServersGetPageSchema,
    ServersPageSchema,
    ServerCreateSchema,
    ServerUpdateSchema,
    ServerUpgradeSchema,
    ServerExecuteSchema,
    ServerStatusSchema
)


class ServersRouterMapper(AbstractServersRouterMapper):
    """
    Mapper for servers router.
    """
    attributes_mapper: AbstractAttributesRouterMapper
    games_mapper: AbstractGamesRouterMapper
    loaders_mapper: AbstractLoadersRouterMapper

    def __init__(
        self,
        attributes_mapper: AbstractAttributesRouterMapper,
        games_mapper: AbstractGamesRouterMapper,
        loaders_mapper: AbstractLoadersRouterMapper
    ):
        self.attributes_mapper = attributes_mapper
        self.games_mapper = games_mapper
        self.loaders_mapper = loaders_mapper

    def dto_to_schema(
        self,
        dto: ServerDto
    ) -> ServerSchema:
        """
        Converts ServerDto object to ServerSchema object.

        Parameters:
        - dto: ServerDto object.

        Returns:
        - ServerSchema: ServerSchema object.
        """
        return ServerSchema(
            id=dto.id,
            name=dto.name,
            version=dto.version,
            game=self.games_mapper.dto_to_short_schema(
                dto=dto.game
            ),
            loader=self.loaders_mapper.dto_to_short_schema(
                dto=dto.loader
            ),
            attributes=self.attributes_mapper.dtos_to_schemas(
                dtos=dto.attributes
            ),
            status=dto.status,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    def dtos_to_schemas(
        self,
        dtos: List[ServerDto]
    ) -> List[ServerSchema]:
        """
        Converts ServerDto objects to ServerSchema objects.

        Parameters:
        - dtos: List of ServerDto objects.

        Returns:
        - List: List of ServerSchema objects.
        """
        return [
            self.dto_to_schema(dto)
            for dto in dtos
        ]

    def page_dto_to_schema(
        self,
        dto: ServersPageDto
    ) -> ServersPageSchema:
        """
        Converts ServersPageDto object to ServersPageSchema object.

        Parameters:
        - dto: ServersPageDto object.

        Returns:
        - ServersPageSchema: ServersPageSchema object.
        """
        return ServersPageSchema(
            servers=self.dtos_to_schemas(
                dtos=dto.servers
            ),
            total=dto.total,
            page=dto.page,
            pages=dto.pages
        )

    def status_dto_to_schema(
        self,
        dto: ServerStatusDto
    ) -> ServerStatusSchema:
        """
        Converts ServerStatusDto object to ServerStatusSchema object.

        Parameters:
        - dto: ServerStatusDto object.

        Returns:
        - ServerStatusSchema: ServerStatusSchema object.
        """
        return ServerStatusSchema(
            running=dto.running,
            port=dto.port
        )

    def get_page_schema_to_dto(
        self,
        schema: ServersGetPageSchema
    ) -> ServersGetPageDto:
        """
        Converts ServersGetPageSchema object to ServersGetPageDto object.

        Parameters:
        - schema: ServersGetPageSchema object.

        Returns:
        - ServersGetPageDto: ServersGetPageDto object.
        """
        return ServersGetPageDto(
            page=schema.page,
            search=schema.search,
            sort_field=schema.sort_field,
            sort_direction=schema.sort_direction,
            limit=schema.limit
        )

    def create_schema_to_dto(
        self,
        schema: ServerCreateSchema
    ) -> ServerCreateDto:
        """
        Converts ServerCreateSchema object to ServerCreateDto object.

        Parameters:
        - schema: ServerCreateSchema object.

        Returns:
        - ServerCreateDto: ServerCreateDto object.
        """
        return ServerCreateDto(
            name=schema.name,
            game_id=schema.game_id,
            loader_id=schema.loader_id,
            version=schema.version
        )

    def update_schema_to_dto(
        self,
        schema: ServerUpdateSchema
    ) -> ServerUpdateDto:
        """
        Converts ServerUpdateSchema object to ServerUpdateDto object.

        Parameters:
        - schema: ServerUpdateSchema object.

        Returns:
        - ServerUpdateDto: ServerUpdateDto object.
        """
        return ServerUpdateDto(
            name=schema.name
        )

    def upgrade_schema_to_dto(
        self,
        schema: ServerUpgradeSchema
    ) -> ServerUpgradeDto:
        """
        Converts ServerUpgradeSchema object to ServerUpgradeDto object.

        Parameters:
        - schema: ServerUpgradeSchema object.

        Returns:
        - ServerUpgradeDto: ServerUpgradeDto object.
        """
        return ServerUpgradeDto(
            version=schema.version
        )

    def execute_schema_to_dto(
        self,
        schema: ServerExecuteSchema
    ) -> ServerExecuteDto:
        """
        Converts ServerExecuteSchema object to ServerExecuteDto object.

        Parameters:
        - schema: ServerExecuteSchema object.

        Returns:
        - ServerExecuteDto: ServerExecuteDto object.
        """
        return ServerExecuteDto(
            command=schema.command
        )
