#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.enums import ServerStateEnum
from domain.value_objects import (
    ServerName,
    ServerVersion
)
from domain.entities import (
    ServerEntity,
    ServersPageEntity,
    ServersGetPageEntity,
    ServerCreateEntity,
    ServerUpdateEntity
)
from application.clients.containers.shared import ContainerStatus
from application.contracts.mappers import (
    AbstractServersServiceMapper,
    AbstractAttributesServiceMapper,
    AbstractGamesServiceMapper,
    AbstractLoadersServiceMapper
)
from application.dtos import (
    ServerDto,
    ServersPageDto,
    ServersGetPageDto,
    ServerCreateDto,
    ServerUpdateDto,
    ServerUpgradeDto,
    ServerStatusDto
)


class ServersServiceMapper(AbstractServersServiceMapper):
    """
    Mapper for servers service.
    """
    attributes_mapper: AbstractAttributesServiceMapper
    games_mapper: AbstractGamesServiceMapper
    loaders_mapper: AbstractLoadersServiceMapper

    def __init__(
        self,
        attributes_mapper: AbstractAttributesServiceMapper,
        games_mapper: AbstractGamesServiceMapper,
        loaders_mapper: AbstractLoadersServiceMapper
    ):
        self.attributes_mapper = attributes_mapper
        self.games_mapper = games_mapper
        self.loaders_mapper = loaders_mapper
    
    def entity_to_dto(
        self,
        entity: ServerEntity
    ) -> ServerDto:
        """
        Converts ServerEntity object to ServerDto object.

        Parameters:
        - entity: ServerEntity object.

        Returns:
        - ServerDto: ServerDto object.
        """
        return ServerDto(
            id=entity.id,
            name=entity.name.value,
            version=entity.version.value,
            game=self.games_mapper.entity_to_dto(
                entity=entity.game
            ),
            loader=self.loaders_mapper.entity_to_dto(
                entity=entity.loader
            ),
            attributes=self.attributes_mapper.entities_to_dtos(
                entities=entity.attributes
            ),
            state=entity.state,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def entities_to_dtos(
        self,
        entities: List[ServerEntity]
    ) -> List[ServerDto]:
        """
        Converts ServerEntity objects to ServerDto objects.

        Parameters:
        - entities: List of ServerEntity objects.

        Returns:
        - List: List of ServerDto objects.
        """
        return [
            self.entity_to_dto(entity)
            for entity in entities
        ]

    def page_entity_to_dto(
        self,
        entity: ServersPageEntity
    ) -> ServersPageDto:
        """
        Converts ServersPageEntity object to ServersPageDto object.

        Parameters:
        - entity: ServersPageEntity object.

        Returns:
        - ServersPageDto: ServersPageDto object.
        """
        return ServersPageDto(
            servers=self.entities_to_dtos(
                entities=entity.servers
            ),
            total=entity.total,
            page=entity.page,
            pages=entity.pages
        )

    def status_dataclass_to_dto(
        self,
        dataclass: ContainerStatus
    ) -> ServerStatusDto:
        """
        Converts ContainerStatus object to ServerStatusDto object.

        Parameters:
        - entity: ContainerStatus object.

        Returns:
        - ServerStatusDto: ServerStatusDto object.
        """
        return ServerStatusDto(
            running=dataclass.running,
            port=dataclass.port
        )

    def get_page_dto_to_entity(
        self,
        dto: ServersGetPageDto
    ) -> ServersGetPageEntity:
        """
        Converts ServersGetPageDto object to ServersGetPageEntity object.

        Parameters:
        - dto: ServersGetPageDto object.

        Returns:
        - ServersGetPageEntity: ServersGetPageEntity object.
        """
        return ServersGetPageEntity(
            page=dto.page,
            search=dto.search,
            sort_field=dto.sort_field,
            sort_direction=dto.sort_direction,
            limit=dto.limit
        )

    def create_dto_to_entity(
        self,
        dto: ServerCreateDto
    ) -> ServerCreateEntity:
        """
        Converts ServerCreateDto object to ServerCreateEntity object.

        Parameters:
        - dto: ServerCreateDto object.

        Returns:
        - ServerCreateEntity: ServerCreateEntity object.
        """
        return ServerCreateEntity(
            name=ServerName(dto.name),
            game_id=dto.game_id,
            loader_id=dto.loader_id,
            version=ServerVersion(dto.version)
        )

    def update_dto_to_entity(
        self,
        server_id: int,
        dto: ServerUpdateDto
    ) -> ServerUpdateEntity:
        """
        Converts ServerUpdateDto object to ServerUpdateEntity object.

        Parameters:
        - server_id: Server ID.
        - dto: ServerUpdateDto object.

        Returns:
        - ServerUpdateEntity: ServerUpdateEntity object.
        """
        return ServerUpdateEntity(
            id=server_id,
            name=ServerName(dto.name) if dto.name is not None else None,
            version=ServerVersion(dto.version) if dto.version is not None else None,
            state=dto.state
        )

    def upgrade_dto_to_update_entity(
        self,
        server_id: int,
        dto: ServerUpgradeDto
    ) -> ServerUpdateEntity:
        """
        Converts ServerUpgradeDto object to ServerUpdateEntity object.

        Parameters:
        - server_id: Server ID.
        - dto: ServerUpdateDto object.

        Returns:
        - ServerUpdateEntity: ServerUpdateEntity object.
        """
        return ServerUpdateEntity(
            id=server_id,
            version=ServerVersion(dto.version),
            state=ServerStateEnum.UPGRADING
        )