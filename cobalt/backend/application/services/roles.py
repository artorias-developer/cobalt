#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from orjson import loads

from domain.exceptions import NotFoundError
from domain.repositories import AbstractRolesRepository
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.clients import AbstractCachesClient
from application.contracts.services import AbstractRolesService
from application.contracts.mappers import AbstractRolesServiceMapper
from application.clients.caches.shared import CacheConstants
from application.dtos import (
    RoleDto,
    RolesGetPageDto,
    RolesPageDto,
    RoleCreateDto,
    RoleUpdateDto
)


class RolesService(AbstractRolesService):
    """
    Roles service.
    """
    caches_client: AbstractCachesClient
    roles_repository: AbstractRolesRepository
    roles_mapper: AbstractRolesServiceMapper
    connections_manager: AbstractConnectionsManager

    def __init__(
        self,
        caches_client: AbstractCachesClient,
        roles_repository: AbstractRolesRepository,
        roles_mapper: AbstractRolesServiceMapper,
        connections_manager: AbstractConnectionsManager
    ):
        self.caches_client = caches_client
        self.roles_repository = roles_repository
        self.roles_mapper = roles_mapper
        self.connections_manager = connections_manager

    async def get_page(
        self,
        dto: RolesGetPageDto
    ) -> RolesPageDto:
        """
        Gets a paginated list of roles.

        Parameters:
        - dto: RolesGetPageDto object.

        Returns:
        - RolesPageDto: RolesPageDto object.
        """
        key = self.caches_client.format_pattern(
            pattern=CacheConstants.ROLES_PAGE_KEY,
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
            return RolesPageDto.from_dict(data)

        mapped_entity = self.roles_mapper.get_page_dto_to_entity(
            dto=dto
        )

        received_entity = await self.roles_repository.get_page(
            entity=mapped_entity
        )

        if not received_entity.roles:
            raise NotFoundError("Roles not found")

        mapped_dto = self.roles_mapper.page_entity_to_dto(
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
        role_id: int
    ) -> RoleDto:
        """
        Gets an existing role by ID.

        Parameters:
        - role_id: Role ID.

        Returns:
        - RoleDto: RoleDto object.
        """
        key = self.caches_client.format_pattern(
            pattern=CacheConstants.ROLES_ITEM_KEY,
            role_id=role_id
        )

        cached = await self.caches_client.get(
            key=key
        )

        if cached:
            data = loads(cached)
            return RoleDto.from_dict(data)

        received_entity = await self.roles_repository.get_one_by_id(
            role_id=role_id
        )

        if not received_entity:
            raise NotFoundError(f"Role {role_id} not found")

        mapped_dto = self.roles_mapper.entity_to_dto(
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
        dto: RoleCreateDto
    ) -> RoleDto:
        """
        Creates a new role.

        Parameters:
        - dto: RoleCreateDto object.

        Returns:
        - RoleDto: RoleDto object.
        """
        mapped_entity = self.roles_mapper.create_dto_to_entity(
            dto=dto
        )

        created_entity = await self.roles_repository.create_one(
            entity=mapped_entity
        )

        await self.caches_client.delete(
            patterns=self.caches_client.format_pattern(
                pattern=CacheConstants.ROLES_PAGE_KEY
            )
        )

        return self.roles_mapper.entity_to_dto(
            entity=created_entity
        )

    async def update_one(
        self,
        role_id: int,
        dto: RoleUpdateDto
    ) -> RoleDto:
        """
        Updates an existing role.

        Parameters:
        - role_id: Role ID.
        - dto: RoleUpdateDto object.

        Returns:
        - RoleDto: RoleDto object.
        """
        mapped_entity = self.roles_mapper.update_dto_to_entity(
            role_id=role_id,
            dto=dto
        )

        updated_entity = await self.roles_repository.update_one(
            entity=mapped_entity
        )

        if not updated_entity:
            raise NotFoundError(f"Role {role_id} not found")

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ROLES_ITEM_KEY,
                    role_id=role_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ROLES_PAGE_KEY
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.USERS_ITEM_KEY,
                    role_id=role_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.USERS_PAGE_KEY
                )
            ]
        )

        connections = await self.connections_manager.get_connections()

        for connection_id, connection in connections.items():
            if connection.state.user.role.id != role_id:
                continue

            await self.connections_manager.disconnect(
                connection_id=connection_id
            )

        return self.roles_mapper.entity_to_dto(
            entity=updated_entity
        )

    async def delete_one(
        self,
        role_id: int
    ) -> None:
        """
        Deletes an existing role.

        Parameters:
        - role_id: Role ID.

        Returns:
        - None.
        """
        deleted_entity = await self.roles_repository.delete_one(
            role_id=role_id
        )

        if not deleted_entity:
            raise NotFoundError(f"Role {role_id} not found")

        await self.caches_client.delete(
            patterns=[
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ROLES_ITEM_KEY,
                    role_id=role_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ROLES_PAGE_KEY
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.USERS_ITEM_KEY,
                    role_id=role_id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.USERS_PAGE_KEY
                )
            ]
        )

    async def delete_many(
        self,
        role_ids: List[int]
    ) -> None:
        """
        Deletes multiple existing roles.

        Parameters:
        - role_ids: List of role IDs.

        Returns:
        - None.
        """
        deleted_entities = await self.roles_repository.delete_many(
            role_ids=role_ids
        )

        if not deleted_entities:
            raise NotFoundError("Roles not found")

        patterns_to_delete = [
            self.caches_client.format_pattern(
                pattern=CacheConstants.ROLES_PAGE_KEY
            ),
            self.caches_client.format_pattern(
                pattern=CacheConstants.USERS_PAGE_KEY
            )
        ]

        for entity in deleted_entities:
            patterns_to_delete.extend([
                self.caches_client.format_pattern(
                    pattern=CacheConstants.ROLES_ITEM_KEY,
                    role_id=entity.id
                ),
                self.caches_client.format_pattern(
                    pattern=CacheConstants.USERS_ITEM_KEY,
                    role_id=entity.id
                )
            ])

        await self.caches_client.delete(
            patterns=patterns_to_delete
        )