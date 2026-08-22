#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from orjson import loads

from domain.exceptions import NotFoundError
from domain.repositories import AbstractLoadersRepository
from application.contracts.clients import AbstractCacheClient
from application.contracts.services import AbstractLoadersService
from application.contracts.mappers import AbstractLoadersServiceMapper
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    LoaderDto,
    LoaderCreateDto,
    LoaderUpdateDto
)


class LoadersService(AbstractLoadersService):
    """
    Loaders service.
    """
    cache_client: AbstractCacheClient
    loaders_repository: AbstractLoadersRepository
    loaders_mapper: AbstractLoadersServiceMapper

    def __init__(
        self,
        cache_client: AbstractCacheClient,
        loaders_repository: AbstractLoadersRepository,
        loaders_mapper: AbstractLoadersServiceMapper
    ):
        self.cache_client = cache_client
        self.loaders_repository = loaders_repository
        self.loaders_mapper = loaders_mapper

    async def get_one_by_id(
            self,
            game_id: int,
            loader_id: int
    ) -> LoaderDto:
        """
        Gets an existing loader by ID.

        Parameters:
        - game_id: Game ID.
        - loader_id: Loader ID.

        Returns:
        - LoaderDto: LoaderDto object.
        """
        key = self.cache_client.format_pattern(
            pattern=CacheConstants.LOADERS_ITEM_KEY,
            loader_id=loader_id,
            game_id=game_id
        )

        cached = await self.cache_client.get(
            key=key
        )

        if cached:
            data = loads(cached)
            return LoaderDto.from_dict(data)

        received_entity = await self.loaders_repository.get_one_by_id(
            loader_id=loader_id,
            game_id=game_id
        )

        if not received_entity:
            raise NotFoundError(
                'Loader {loader_id} for game {game_id} not found',
                loader_id=loader_id,
                game_id=game_id
            )

        key = self.cache_client.format_pattern(
            pattern=CacheConstants.LOADERS_ITEM_KEY,
            loader_id=received_entity.id,
            name=received_entity.name.value,
            game_id=received_entity.game_id
        )

        mapped_dto = self.loaders_mapper.entity_to_dto(
            entity=received_entity
        )

        await self.cache_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.TTL_1_HOUR
        )

        return mapped_dto

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
        key = self.cache_client.format_pattern(
            pattern=CacheConstants.LOADERS_ITEM_KEY,
            name=name,
            game_id=game_id
        )

        cached = await self.cache_client.get(
            key=key
        )

        if cached:
            data = loads(cached)
            return LoaderDto.from_dict(data)

        received_entity = await self.loaders_repository.get_one_by_name(
            name=name,
            game_id=game_id
        )

        if not received_entity:
            raise NotFoundError(
                'Loader "{name}" for game {game_id} not found',
                name=name,
                game_id=game_id
            )

        key = self.cache_client.format_pattern(
            pattern=CacheConstants.LOADERS_ITEM_KEY,
            loader_id=received_entity.id,
            name=received_entity.name.value,
            game_id=received_entity.game_id
        )

        mapped_dto = self.loaders_mapper.entity_to_dto(
            entity=received_entity
        )

        await self.cache_client.set(
            key=key,
            value=mapped_dto.model_dump_json(),
            expire=CacheConstants.TTL_1_HOUR
        )

        return mapped_dto

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
        mapped_entity = self.loaders_mapper.create_dto_to_entity(
            dto=dto
        )

        created_entity = await self.loaders_repository.create_one(
            game_id=game_id,
            entity=mapped_entity
        )

        await self.cache_client.delete(
            patterns=[
                self.cache_client.format_pattern(
                    pattern=CacheConstants.GAMES_ITEM_KEY,
                    game_id=created_entity.game_id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.GAMES_PAGE_KEY
                )
            ]
        )

        return self.loaders_mapper.entity_to_dto(
            entity=created_entity
        )

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
        mapped_entity = self.loaders_mapper.update_dto_to_entity(
            dto=dto
        )

        updated_entity = await self.loaders_repository.update_one(
            game_id=game_id,
            entity=mapped_entity
        )

        if not updated_entity:
            raise NotFoundError("Loader {loader_id} not found", loader_id=mapped_entity.id)

        await self.cache_client.delete(
            patterns=[
                self.cache_client.format_pattern(
                    pattern=CacheConstants.LOADERS_ITEM_KEY,
                    loader_id=updated_entity.id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.GAMES_ITEM_KEY,
                    game_id=updated_entity.game_id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.GAMES_PAGE_KEY
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    loader_id=updated_entity.id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )

        return self.loaders_mapper.entity_to_dto(
            entity=updated_entity
        )

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
        deleted_entity = await self.loaders_repository.delete_one(
            game_id=game_id,
            loader_id=loader_id
        )

        if not deleted_entity:
            raise NotFoundError("Loader {loader_id} not found", loader_id=loader_id)

        await self.cache_client.delete(
            patterns=[
                self.cache_client.format_pattern(
                    pattern=CacheConstants.LOADERS_ITEM_KEY,
                    loader_id=loader_id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.GAMES_ITEM_KEY,
                    game_id=deleted_entity.game_id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.GAMES_PAGE_KEY
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    loader_id=loader_id
                ),
                self.cache_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )