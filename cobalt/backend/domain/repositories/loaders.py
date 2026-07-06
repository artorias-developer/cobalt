#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, Any

from domain.entities import (
    LoaderEntity,
    LoaderCreateEntity,
    LoaderUpdateEntity
)


class AbstractLoadersRepository(ABC):
    """
    Abstract loaders repository.
    """

    @abstractmethod
    async def get_one_by_name(
        self,
        name: str,
        game_id: int,
        session: Optional[Any] = None
    ) -> Optional[LoaderEntity]:
        """
        Gets an existing loader by name.

        Parameters:
        - name: Name of the loader.
        - game_id: Game Loader ID.
        - session: Session object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        ...

    @abstractmethod
    async def create_one(
        self,
        game_id: int,
        entity: LoaderCreateEntity,
        session: Optional[Any] = None
    ) -> LoaderEntity:
        """
        Creates a new loader.

        Parameters:
        - game_id: Game ID.
        - entity: LoaderCreateEntity object.
        - session: Session object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        ...

    @abstractmethod
    async def update_one(
        self,
        game_id: int,
        entity: LoaderUpdateEntity,
        session: Optional[Any] = None
    ) -> Optional[LoaderEntity]:
        """
        Updates an existing loader.

        Parameters:
        - game_id: Game ID.
        - entity: LoaderUpdateEntity object.
        - session: Session object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        ...

    @abstractmethod
    async def delete_one(
        self,
        game_id: int,
        loader_id: int,
        session: Optional[Any] = None
    ) -> Optional[LoaderEntity]:
        """
        Deletes an existing loader.

        Parameters:
        - game_id: Game ID.
        - loader_id: Loader ID.
        - session: Session object.

        Returns:
        - LoaderEntity: LoaderEntity object.
        """
        ...