#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List

from domain.entities import (
    ServerEntity,
    ServersPageEntity,
    ServersGetPageEntity,
    ServerCreateEntity,
    ServerUpdateEntity
)
from application.clients.containers.shared import ContainerStatus
from application.dtos import (
    ServerDto,
    ServersPageDto,
    ServersGetPageDto,
    ServerCreateDto,
    ServerUpdateDto,
    ServerStatusDto
)


class AbstractServersServiceMapper(ABC):
    """
    Abstract mapper for servers service.
    """

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def status_dataclass_to_dto(
        self,
        dataclass: ContainerStatus
    ) -> ServerStatusDto:
        """
        Converts ContainerStatus object to ServerStatusDto object.

        Parameters:
        - dataclass: ContainerStatus object.

        Returns:
        - ServerStatusDto: ServerStatusDto object.
        """
        ...
