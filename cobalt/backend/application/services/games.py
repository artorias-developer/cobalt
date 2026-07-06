#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Callable

from orjson import loads

from domain.exceptions import NotFoundError
from domain.repositories import AbstractGamesRepository
from application.contracts.managers import AbstractI18nManager
from application.contracts.clients import AbstractCachesClient
from application.contracts.services import AbstractGamesService
from application.contracts.mappers import AbstractGamesServiceMapper
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    GameDto,
    GamesGetPageDto,
    GamesPageDto,
    GameCreateDto,
    GameUpdateDto
)


class GamesService(AbstractGamesService):
    """
    Games service.
    """
    caches_client: AbstractCachesClient
    games_repository: AbstractGamesRepository
    games_mapper: AbstractGamesServiceMapper
    i18n_manager: AbstractI18nManager

    _: Callable

    def __init__(
        self,
        caches_client: AbstractCachesClient,
        games_repository: AbstractGamesRepository,
        games_mapper: AbstractGamesServiceMapper,
        i18n_manager: AbstractI18nManager
    ):
        self.caches_client = caches_client
        self.games_repository = games_repository
        self.games_mapper = games_mapper
        self.i18n_manager = i18n_manager

        self._ = i18n_manager.gettext

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
        key = self.caches_client.format_pattern(
            pattern=CacheConstants.GAMES_PAGE_KEY,
            page=dto.page,
            search=dto.search,
            sort_field=dto.sort_field,
            sort_direction=dto.sort_direction,
            limit=dto.limit
        )

        cached = await self.caches_client.get(
            key=key
        )

        if cached:
            data = loads(cached)
            return GamesPageDto.from_dict(data)

        mapped_entity = self.games_mapper.get_page_dto_to_entity(
            dto=dto
        )

        received_entity = await self.games_repository.get_page(
            entity=mapped_entity
        )

        if not received_entity.games:
            raise NotFoundError(self._("Game not found"))

        mapped_dto = self.games_mapper.page_entity_to_dto(
            entity=received_entity
        )

        await self.caches_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.NORMAL_TTL_SECONDS
        )

        return mapped_dto

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
        key = self.caches_client.format_pattern(
            pattern=CacheConstants.GAMES_ITEM_KEY,
            game_id=game_id
        )

        cached = await self.caches_client.get(
            key=key
        )

        if cached:
            data = loads(cached)
            return GameDto.from_dict(data)

        received_entity = await self.games_repository.get_one_by_id(
            game_id=game_id
        )

        if not received_entity:
            raise NotFoundError(self._("Game {game_id} not found").format(game_id=game_id))

        key = self.caches_client.format_pattern(
            pattern=CacheConstants.GAMES_ITEM_KEY,
            game_id=received_entity.id,
            name=received_entity.name
        )

        mapped_dto = self.games_mapper.entity_to_dto(
            entity=received_entity
        )

        await self.caches_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.NORMAL_TTL_SECONDS
        )

        return mapped_dto

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
        key = self.caches_client.format_pattern(
            pattern=CacheConstants.GAMES_ITEM_KEY,
            name=name
        )

        cached = await self.caches_client.get(
            key=key
        )

        if cached:
            data = loads(cached)
            return GameDto.from_dict(data)

        received_entity = await self.games_repository.get_one_by_name(
            name=name
        )

        if not received_entity:
            raise NotFoundError(self._('Game "{name}" not found').format(name=name))

        key = self.caches_client.format_pattern(
            pattern=CacheConstants.GAMES_ITEM_KEY,
            game_id=received_entity.id,
            name=name
        )

        mapped_dto = self.games_mapper.entity_to_dto(
            entity=received_entity
        )

        await self.caches_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.NORMAL_TTL_SECONDS
        )

        return mapped_dto

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
        mapped_entity = self.games_mapper.create_dto_to_entity(
            dto=dto
        )

        created_entity = await self.games_repository.create_one(
            entity=mapped_entity
        )

        await self.caches_client.delete(
            patterns=self.caches_client.format_pattern(
                pattern=CacheConstants.GAMES_PAGE_KEY
            )
        )

        return self.games_mapper.entity_to_dto(
            entity=created_entity
        )

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
        mapped_entity = self.games_mapper.update_dto_to_entity(
            game_id=game_id,
            dto=dto
        )

        updated_entity = await self.games_repository.update_one(
            entity=mapped_entity
        )

        if not updated_entity:
            raise NotFoundError(self._("Game {game_id} not found").format(game_id=game_id))

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.GAMES_ITEM_KEY,
                    game_id=game_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.GAMES_PAGE_KEY
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    game_id=game_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )

        return self.games_mapper.entity_to_dto(
            entity=updated_entity
        )

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
        deleted_entity = await self.games_repository.delete_one(
            game_id=game_id
        )

        if not deleted_entity:
            raise NotFoundError(self._("Game {game_id} not found").format(game_id=game_id))

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.GAMES_ITEM_KEY,
                    game_id=game_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.GAMES_PAGE_KEY
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    game_id=game_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )