#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Callable

from orjson import loads

from domain.exceptions import (
    NotFoundError,
    ValidationError
)
from domain.repositories import AbstractAttributesRepository
from application.contracts.managers import AbstractI18nManager
from application.contracts.clients import AbstractCachesClient
from application.contracts.services import AbstractAttributesService
from application.contracts.mappers import AbstractAttributesServiceMapper
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    AttributeDto,
    AttributesGetPageDto,
    AttributesPageDto,
    AttributeCreateDto,
    AttributeUpdateDto
)


class AttributesService(AbstractAttributesService):
    """
    Attributes service.
    """
    caches_client: AbstractCachesClient
    attributes_repository: AbstractAttributesRepository
    attributes_mapper: AbstractAttributesServiceMapper
    i18n_manager: AbstractI18nManager

    _: Callable

    def __init__(
        self,
        caches_client: AbstractCachesClient,
        attributes_repository: AbstractAttributesRepository,
        attributes_mapper: AbstractAttributesServiceMapper,
        i18n_manager: AbstractI18nManager
    ):
        self.caches_client = caches_client
        self.attributes_repository = attributes_repository
        self.attributes_mapper = attributes_mapper
        self.i18n_manager = i18n_manager

        self._ = i18n_manager.gettext

    async def get_page(
        self,
        server_id: int,
        dto: AttributesGetPageDto
    ) -> AttributesPageDto:
        """
        Gets a paginated list of attributes.

        Parameters:
        - server_id: Server ID.
        - dto: AttributesGetPageDto object.

        Returns:
        - AttributesPageDto: AttributesPageDto object.
        """
        key = self.caches_client.format_pattern(
            pattern=CacheConstants.ATTRIBUTES_PAGE_KEY,
            server_id=server_id,
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
            return AttributesPageDto.from_dict(data)

        mapped_entity = self.attributes_mapper.get_page_dto_to_entity(
            dto=dto
        )

        received_entity = await self.attributes_repository.get_page(
            server_id=server_id,
            entity=mapped_entity
        )

        if not received_entity.attributes:
            raise NotFoundError(self._("Server or attributes not found"))

        mapped_dto = self.attributes_mapper.page_entity_to_dto(
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
        server_id: int,
        attribute_id: int
    ) -> AttributeDto:
        """
        Gets an existing attribute by ID.

        Parameters:
        - server_id: Server ID.
        - attribute_id: Attribute ID.

        Returns:
        - AttributeDto: AttributeDto object.
        """
        search_key = self.caches_client.format_pattern(
            pattern=CacheConstants.ATTRIBUTES_ITEM_KEY,
            attribute_id=attribute_id,
            server_id=server_id
        )

        cached = await self.caches_client.get(
            pattern=search_key
        )

        if cached:
            data = loads(cached)
            return AttributeDto.from_dict(data)

        received_entity = await self.attributes_repository.get_one_by_id(
            server_id=server_id,
            attribute_id=attribute_id
        )

        if not received_entity:
            raise NotFoundError(
                self._("Server {server_id} or attribute {attribute_id} not found").format(
                    server_id=server_id,
                    attribute_id=attribute_id
                )
            )

        key = self.caches_client.format_pattern(
            pattern=CacheConstants.ATTRIBUTES_ITEM_KEY,
            attribute_id=received_entity.id,
            key=received_entity.key,
            server_id=received_entity.server_id
        )

        mapped_dto = self.attributes_mapper.entity_to_dto(
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
        server_id: int,
        dto: AttributeCreateDto
    ) -> AttributeDto:
        """
        Creates a new attribute.

        Parameters:
        - server_id: Server ID.
        - dto: AttributeCreateDto object.

        Returns:
        - AttributeDto: AttributeDto object.
        """
        mapped_entity = self.attributes_mapper.create_dto_to_entity(
            dto=dto
        )

        crated_entity = await self.attributes_repository.create_one(
            server_id=server_id,
            entity=mapped_entity
        )

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_PAGE_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )

        return self.attributes_mapper.entity_to_dto(
            entity=crated_entity
        )

    async def create_many(
        self,
        server_id: int,
        dtos: List[AttributeCreateDto]
    ) -> List[AttributeDto]:
        """
        Creates the new attributes.

        Parameters:
        - server_id: Server ID.
        - dtos: List of AttributeCreateDto objects.

        Returns:
        - List: List of AttributeDto objects.
        """
        mapped_entities = self.attributes_mapper.create_dtos_to_entities(
            dtos=dtos
        )

        crated_entities = await self.attributes_repository.create_many(
            server_id=server_id,
            entities=mapped_entities
        )

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_PAGE_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )

        return self.attributes_mapper.entities_to_dtos(
            entities=crated_entities
        )

    async def update_one(
        self,
        server_id: int,
        dto: AttributeUpdateDto
    ) -> AttributeDto:
        """
        Updates an existing attribute.

        Parameters:
        - server_id: Server ID.
        - dto: AttributeUpdateDto object.

        Returns:
        - AttributeDto: AttributeDto object.
        """
        if dto.key is None and dto.value is None:
            raise ValidationError(self._("At least one field (key or value) must be provided"))

        mapped_entity = self.attributes_mapper.update_dto_to_entity(
            dto=dto
        )

        updated_entity = await self.attributes_repository.update_one(
            server_id=server_id,
            entity=mapped_entity
        )

        if not updated_entity:
            raise NotFoundError(self._("Server or attribute not found"))

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_ITEM_KEY,
                    attribute_id=updated_entity.id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_PAGE_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )

        return self.attributes_mapper.entity_to_dto(
            entity=updated_entity
        )

    async def update_many(
        self,
        server_id: int,
        dtos: List[AttributeUpdateDto]
    ) -> List[AttributeDto]:
        """
        Updates an existing attributes.

        Parameters:
        - server_id: Server ID.
        - dtos: List of AttributeUpdateDto objects.

        Returns:
        - List: List of AttributeDto objects.
        """
        mapped_entities = self.attributes_mapper.update_dtos_to_entities(
            dtos=dtos
        )

        updated_entities = await self.attributes_repository.update_many(
            server_id=server_id,
            entities=mapped_entities
        )

        if not updated_entities:
            raise NotFoundError(self._("Server or attributes not found"))

        patterns_to_delete = [
            self.caches_client.format_pattern(
                pattern=CacheConstants.ATTRIBUTES_PAGE_KEY,
                server_id=server_id
            ),
            self.caches_client.format_pattern(
                pattern=CacheConstants.SERVERS_ITEM_KEY,
                server_id=server_id
            ),
            self.caches_client.format_pattern(
                pattern=CacheConstants.SERVERS_PAGE_KEY
            )
        ]

        for entity in updated_entities:
            patterns_to_delete.append(
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_ITEM_KEY,
                    attribute_id=entity.id
                )
            )

        await self.caches_client.delete(
            patterns=patterns_to_delete
        )

        return self.attributes_mapper.entities_to_dtos(
            entities=updated_entities
        )

    async def delete_one(
        self,
        server_id: int,
        attribute_id: int
    ) -> None:
        """
        Deletes an existing attributes.

        Parameters:
        - server_id: Server ID.
        - attribute_id: Attribute ID.

        Returns:
        - None.
        """
        deleted_entity = await self.attributes_repository.delete_one(
            server_id=server_id,
            attribute_id=attribute_id
        )

        if not deleted_entity:
            raise NotFoundError(self._("Server or attribute not found"))

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_ITEM_KEY,
                    attribute_id=deleted_entity.id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_PAGE_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_ITEM_KEY,
                    server_id=server_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.SERVERS_PAGE_KEY
                )
            ]
        )

    async def delete_many(
        self,
        server_id: int,
        attribute_ids: List[int]
    ) -> None:
        """
        Deletes an existing attributes.

        Parameters:
        - server_id: Server ID.
        - attribute_ids: List of attribute IDs.

        Returns:
        - None.
        """
        deleted_entities = await self.attributes_repository.delete_many(
            server_id=server_id,
            attribute_ids=attribute_ids
        )

        if not deleted_entities:
            raise NotFoundError(self._("Server or attributes not found"))

        patterns_to_delete = [
            self.caches_client.format_pattern(
                pattern=CacheConstants.ATTRIBUTES_PAGE_KEY,
                server_id=server_id
            ),
            self.caches_client.format_pattern(
                pattern=CacheConstants.SERVERS_ITEM_KEY,
                server_id=server_id
            ),
            self.caches_client.format_pattern(
                pattern=CacheConstants.SERVERS_PAGE_KEY
            )
        ]

        for entity in deleted_entities:
            patterns_to_delete.append(
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ATTRIBUTES_ITEM_KEY,
                    attribute_id=entity.id
                )
            )

        await self.caches_client.delete(
            patterns=patterns_to_delete
        )
