#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, List, Any

from domain.entities import (
    ServerEntity,
    ServersPageEntity,
    ServersGetPageEntity,
    ServerCreateEntity,
    ServerUpdateEntity
)


class AbstractServersRepository(ABC):
    """
    Abstract servers repository.
    """

    @abstractmethod
    async def get_page(
        self,
        entity: ServersGetPageEntity,
        session: Optional[Any] = None
    ) -> ServersPageEntity:
        """
        Gets a paginated list of servers.

        Parameters:
        - entity: ServersGetPageEntity object.
        - session: Session object.

        Returns:
        - ServersPageEntity: ServersPageEntity object.
        """
        ...

    @abstractmethod
    async def get_one_by_id(
        self,
        server_id: int,
        session: Optional[Any] = None
    ) -> Optional[ServerEntity]:
        """
        Gets an existing server by ID.

        Parameters:
        - server_id: Server ID.
        - session: Session object.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        ...

    @abstractmethod
    async def get_many_by_ids(
        self,
        server_ids: List[int],
        session: Optional[Any] = None
    ) -> List[ServerEntity]:
        """
        Gets multiple existing servers by IDs.

        Parameters:
        - server_ids: List of server IDs.
        - session: Session object.

        Returns:
        - List: List of ServerEntity objects.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        entity: ServerCreateEntity,
        session: Optional[Any] = None
    ) -> ServerEntity:
        """
        Creates a new server.

        Parameters:
        - entity: ServerCreateEntity object.
        - session: Session object.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        entity: ServerUpdateEntity,
        session: Optional[Any] = None
    ) -> Optional[ServerEntity]:
        """
        Updates an existing server.

        Parameters:
        - entity: ServerUpdateEntity object.
        - session: Session object.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        server_id: int,
        session: Optional[Any] = None
    ) -> Optional[ServerEntity]:
        """
        Deletes an existing server.

        Parameters:
        - server_id: Server ID.
        - session: Session object.

        Returns:
        - ServerEntity: ServerEntity object.
        """
        ...

    @abstractmethod
    async def delete_many(
        self,
        server_ids: List[int],
        session: Optional[Any] = None
    ) -> List[ServerEntity]:
        """
        Deletes multiple existing servers.

        Parameters:
        - server_ids: List of server IDs.
        - session: Session object.

        Returns:
        - List: List of ServerEntity objects.
        """
        ...