#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from application.dtos import (
    ServerDto,
    ServersGetPageDto,
    ServersPageDto,
    ServerCreateDto,
    ServerUpdateDto,
    ServerExecuteDto,
    ServerStatusDto
)


class AbstractServersRouterMapper(ABC):
    """
    Abstract mapper for servers router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: ServerDto
    ) -> Any:
        """
        Converts ServerDto object to schema object.

        Parameters:
        - dto: ServerDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def dtos_to_schemas(
        self,
        dtos: List[ServerDto]
    ) -> List[Any]:
        """
        Converts ServerDto objects to schema objects.

        Parameters:
        - dtos: List of ServerDto objects.

        Returns:
        - List: List of any schema objects.
        """
        ...

    @abstractmethod
    def page_dto_to_schema(
        self,
        dto: ServersPageDto
    ) -> Any:
        """
        Converts ServersPageDto object to schema object.

        Parameters:
        - dto: ServersPageDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def status_dto_to_schema(
        self,
        dto: ServerStatusDto
    ) -> Any:
        """
        Converts ServerStatusDto object to schema object.

        Parameters:
        - dto: ServerStatusDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def get_page_schema_to_dto(
        self,
        schema: Any
    ) -> ServersGetPageDto:
        """
        Converts schema object to ServersGetPageDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - ServersGetPageDto: ServersGetPageDto object.
        """
        ...

    @abstractmethod
    def create_schema_to_dto(
        self,
        schema: Any
    ) -> ServerCreateDto:
        """
        Converts schema object to ServerCreateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - ServerCreateDto: ServerCreateDto object.
        """
        ...

    @abstractmethod
    def update_schema_to_dto(
        self,
        schema: Any
    ) -> ServerUpdateDto:
        """
        Converts schema object to ServerUpdateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - ServerUpdateDto: ServerUpdateDto object.
        """
        ...

    @abstractmethod
    def execute_schema_to_dto(
        self,
        schema: Any
    ) -> ServerExecuteDto:
        """
        Converts schema object to ServerExecuteDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - ServerExecuteDto: ServerExecuteDto object.
        """
        ...
