#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List

from domain.entities import (
    GameEntity,
    GamesPageEntity,
    GamesGetPageEntity,
    GameCreateEntity,
    GameUpdateEntity
)
from application.dtos import (
    GameDto,
    GamesPageDto,
    GamesGetPageDto,
    GameCreateDto,
    GameUpdateDto
)


class AbstractGamesServiceMapper(ABC):
    """
    Abstract mapper for games service.
    """

    @abstractmethod
    def entity_to_dto(
        self,
        entity: GameEntity
    ) -> GameDto:
        """
        Converts GameEntity object to GameDto object.

        Parameters:
        - entity: GameEntity object.

        Returns:
        - GameDto: GameDto object.
        """
        ...

    @abstractmethod
    def entities_to_dtos(
        self,
        entities: List[GameEntity]
    ) -> List[GameDto]:
        """
        Converts GameEntity objects to GameDto objects.

        Parameters:
        - entities: List of GameEntity objects.

        Returns:
        - List: List of GameDto objects.
        """
        ...

    @abstractmethod
    def page_entity_to_dto(
        self,
        entity: GamesPageEntity
    ) -> GamesPageDto:
        """
        Converts GamesPageEntity object to GamesPageDto object.

        Parameters:
        - entity: GamesPageEntity object.

        Returns:
        - GamesPageDto: GamesPageDto object.
        """
        ...

    @abstractmethod
    def get_page_dto_to_entity(
        self,
        dto: GamesGetPageDto
    ) -> GamesGetPageEntity:
        """
        Converts GamesGetPageDto object to GamesGetPageEntity object.

        Parameters:
        - dto: GamesGetPageDto object.

        Returns:
        - GamesGetPageEntity: GamesGetPageEntity object.
        """
        ...

    @abstractmethod
    def create_dto_to_entity(
        self,
        dto: GameCreateDto
    ) -> GameCreateEntity:
        """
        Converts GameCreateDto object to GameCreateEntity object.

        Parameters:
        - dto: GameCreateDto object.

        Returns:
        - GameCreateEntity: GameCreateEntity object.
        """
        ...

    @abstractmethod
    def update_dto_to_entity(
        self,
        game_id: int,
        dto: GameUpdateDto
    ) -> GameUpdateEntity:
        """
        Converts GameUpdateDto object to GameUpdateEntity object.

        Parameters:
        - game_id: Game ID.
        - dto: GameUpdateDto object.

        Returns:
        - GameUpdateEntity: GameUpdateEntity object.
        """
        ...
