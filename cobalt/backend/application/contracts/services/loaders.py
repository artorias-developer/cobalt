#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC

from application.dtos import (
    LoaderDto,
    LoaderCreateDto,
    LoaderUpdateDto
)


class AbstractLoadersService(ABC):
    """
    Abstract loaders service.
    """

    @abstractmethod
    async def get_one_by_name(
        self,
        game_id: int,
        name: str
    ) -> LoaderDto:
        """
        Gets an existing loader by name.

        Parameters:
        - game_id: Game ID.
        - name: Loader name.

        Returns:
        - LoaderDto: LoaderDto object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        game_id: int,
        dto: LoaderCreateDto
    ) -> LoaderDto:
        """
        Creates a new loader.

        Parameters:
        - game_id: Game ID.
        - dto: LoaderCreateDto object.

        Returns:
        - LoaderDto: LoaderDto object.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        game_id: int,
        dto: LoaderUpdateDto
    ) -> LoaderDto:
        """
        Updates an existing loader.

        Parameters:
        - game_id: Game ID.
        - dto: LoaderUpdateDto object.

        Returns:
        - LoaderDto: LoaderDto object.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        game_id: int,
        loader_id: int
    ) -> None:
        """
        Deletes an existing loader.

        Parameters:
        - game_id: Game ID.
        - loader_id: Loader ID.

        Returns:
        - None.
        """
        ...