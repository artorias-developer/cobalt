#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC

from application.dtos import (
    GameDto,
    GamesGetPageDto,
    GamesPageDto,
    GameCreateDto,
    GameUpdateDto
)


class AbstractGamesService(ABC):
    """
    Abstract games service.
    """

    @abstractmethod
    async def get_page(
        self,
        dto: GamesGetPageDto
    ) -> GamesPageDto:
        """
        Gets a paginated list of games.

        Parameters:
        - dto: GamesGetPageDto object.

        Returns:
        - GamesPageDto: GamesPageDto object.
        """
        ...

    @abstractmethod
    async def get_one_by_id(
        self,
        game_id: int
    ) -> GameDto:
        """
        Gets an existing game by ID.

        Parameters:
        - game_id: Game ID.

        Returns:
        - GameDto: GameDto object.
        """
        ...

    @abstractmethod
    async def get_one_by_name(
        self,
        name: str
    ) -> GameDto:
        """
        Gets an existing game by name.

        Parameters:
        - name: Game name.

        Returns:
        - GameDto: GameDto object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        dto: GameCreateDto
    ) -> GameDto:
        """
        Creates a new game.

        Parameters:
        - dto: GameCreateDto object.

        Returns:
        - GameDto: GameDto object.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        game_id: int,
        dto: GameUpdateDto
    ) -> GameDto:
        """
        Updates an existing game.

        Parameters:
        - game_id: Game ID.
        - dto: GameUpdateDto object.

        Returns:
        - GameDto: GameDto object.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        game_id: int
    ) -> None:
        """
        Deletes an existing game.

        Parameters:
        - game_id: Game ID.

        Returns:
        - None.
        """
        ...