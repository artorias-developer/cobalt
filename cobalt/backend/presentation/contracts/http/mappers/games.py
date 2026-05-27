#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, List

from application.dtos import (
    GameDto,
    GamesGetPageDto,
    GamesPageDto
)


class AbstractGamesRouterMapper(ABC):
    """
    Abstract mapper for games router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: GameDto
    ) -> Any:
        """
        Converts GameDto object to schema object.

        Parameters:
        - dto: GameDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def dtos_to_schemas(
        self,
        dtos: List[GameDto]
    ) -> List[Any]:
        """
        Converts GameDto objects to schema objects.

        Parameters:
        - dtos: List of GameDto objects.

        Returns:
        - List: List of any schema objects.
        """
        ...

    @abstractmethod
    def dto_to_short_schema(
        self,
        dto: GameDto
    ) -> Any:
        """
        Converts GameDto object to short schema object.

        Parameters:
        - dto: GameDto object.

        Returns:
        - Any: Server schema object.
        """
        ...

    @abstractmethod
    def page_dto_to_schema(
        self,
        dto: GamesPageDto
    ) -> Any:
        """
        Converts GamesPageDto object to schema object.

        Parameters:
        - dto: GamesPageDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def get_page_schema_to_dto(
        self,
        schema: Any
    ) -> GamesGetPageDto:
        """
        Converts schema object to GamesGetPageDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - GamesGetPageDto: GamesGetPageDto object.
        """
        ...
