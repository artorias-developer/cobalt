#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, Any

from domain.entities import (
    GameEntity,
    GamesPageEntity,
    GameCreateEntity,
    GameUpdateEntity,
    GamesGetPageEntity
)


class AbstractGamesRepository(ABC):
    """
    Abstract games repository.
    """

    @abstractmethod
    async def get_page(
        self,
        entity: GamesGetPageEntity,
        session: Optional[Any] = None
    ) -> GamesPageEntity:
        """
        Gets a paginated list of games.

        Parameters:
        - entity: GamesGetPageEntity object.
        - session: Session object.

        Returns:
        - GamesPageEntity: GamesPageEntity object.
        """
        ...

    @abstractmethod
    async def get_one_by_id(
        self,
        game_id: int,
        session: Optional[Any] = None
    ) -> Optional[GameEntity]:
        """
        Gets an existing game by ID.

        Parameters:
        - game_id: Game ID.
        - session: Session object.

        Returns:
        - GameEntity: GameEntity object.
        """
        ...

    @abstractmethod
    async def get_one_by_name(
        self,
        name: str,
        session: Optional[Any] = None
    ) -> Optional[GameEntity]:
        """
        Gets an existing game by name.

        Parameters:
        - name: Name of the game.
        - session: Session object.

        Returns:
        - GameEntity: GameEntity object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        entity: GameCreateEntity,
        session: Optional[Any] = None
    ) -> GameEntity:
        """
        Creates a new game.

        Parameters:
        - entity: GameCreateEntity object.
        - session: Session object.

        Returns:
        - GameEntity: GameEntity object.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        entity: GameUpdateEntity,
        session: Optional[Any] = None
    ) -> Optional[GameEntity]:
        """
        Updates an existing game.

        Parameters:
        - entity: GameUpdateEntity object.
        - session: Session object.

        Returns:
        - GameEntity: GameEntity object.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        game_id: int,
        session: Optional[Any] = None
    ) -> Optional[GameEntity]:
        """
        Deletes an existing game.

        Parameters:
        - game_id: Game ID.
        - session: Session object.

        Returns:
        - GameEntity: GameEntity object.
        """
        ...