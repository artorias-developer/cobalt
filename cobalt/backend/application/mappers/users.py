#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, List

from domain.value_objects import (
    UserLogin,
    HashedPassword,
    Salt
)
from domain.entities import (
    UserEntity,
    UsersPageEntity,
    UsersGetPageEntity,
    UserCreateEntity,
    UserUpdateEntity
)
from application.contracts.mappers import (
    AbstractUsersServiceMapper,
    AbstractRolesServiceMapper,
    AbstractSettingsServiceMapper
)
from application.dtos import (
    UserDto,
    UsersPageDto,
    UsersGetPageDto,
    UserCreateDto,
    UserUpdateDto
)


class UsersServiceMapper(AbstractUsersServiceMapper):
    """
    Mapper for users service.
    """
    roles_mapper: AbstractRolesServiceMapper
    settings_mapper: AbstractSettingsServiceMapper

    def __init__(
        self,
        roles_mapper: AbstractRolesServiceMapper,
        settings_mapper: AbstractSettingsServiceMapper
    ):
        self.roles_mapper = roles_mapper
        self.settings_mapper = settings_mapper

    def entity_to_dto(
        self,
        entity: UserEntity
    ) -> UserDto:
        """
        Converts UserEntity object to UserDto object.

        Parameters:
        - entity: UserEntity object.

        Returns:
        - UserDto: UserDto object.
        """
        return UserDto(
            id=entity.id,
            login=entity.login.value,
            hashed_password=entity.hashed_password.value,
            salt=entity.salt.value,
            role=self.roles_mapper.entity_to_dto(
                entity=entity.role
            ),
            settings=self.settings_mapper.entity_to_dto(
                entity=entity.settings
            ),
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def entities_to_dtos(
        self,
        entities: List[UserEntity]
    ) -> List[UserDto]:
        """
        Converts UserEntity objects to UserDto objects.

        Parameters:
        - entities: List of UserEntity objects.

        Returns:
        - List: List of UserDto objects.
        """
        return [
            self.entity_to_dto(entity)
            for entity in entities
        ]

    def page_entity_to_dto(
        self,
        entity: UsersPageEntity
    ) -> UsersPageDto:
        """
        Converts UsersPageEntity object to UsersPageDto object.

        Parameters:
        - entity: UsersPageEntity object.

        Returns:
        - UsersPageDto: UsersPageDto object.
        """
        return UsersPageDto(
            users=self.entities_to_dtos(
                entities=entity.users
            ),
            total=entity.total,
            page=entity.page,
            pages=entity.pages
        )

    def get_page_dto_to_entity(
        self,
        dto: UsersGetPageDto
    ) -> UsersGetPageEntity:
        """
        Converts UsersGetPageDto object to UsersGetPageEntity object.

        Parameters:
        - dto: UsersGetPageDto object.

        Returns:
        - UsersGetPageEntity: UsersGetPageEntity object.
        """
        return UsersGetPageEntity(
            page=dto.page,
            search=dto.search,
            sort_field=dto.sort_field,
            sort_direction=dto.sort_direction,
            limit=dto.limit
        )

    def create_dto_to_entity(
        self,
        dto: UserCreateDto,
        hashed_password: str,
        salt: str
    ) -> UserCreateEntity:
        """
        Converts UserCreateDto object to UserCreateEntity object.

        Parameters:
        - dto: UserCreateDto object.
        - hashed_password: Hashed password.
        - salt: User salt.

        Returns:
        - UserCreateEntity: UserCreateEntity object.
        """
        return UserCreateEntity(
            login=UserLogin(dto.login),
            hashed_password=HashedPassword(hashed_password),
            salt=Salt(salt),
            role_id=dto.role_id
        )

    def update_dto_to_entity(
        self,
        user_id: int,
        dto: UserUpdateDto,
        hashed_password: Optional[str] = None,
        salt: Optional[str] = None
    ) -> UserUpdateEntity:
        """
        Converts UserUpdateDto object to UserUpdateEntity object.

        Parameters:
        - user_id: User ID.
        - dto: UserUpdateDto object.
        - hashed_password: Hashed password.
        - salt: Password hashing salt.

        Returns:
        - UserUpdateEntity: UserUpdateEntity object.
        """
        return UserUpdateEntity(
            id=user_id,
            login=UserLogin(dto.login) if dto.login is not None else None,
            hashed_password=HashedPassword(hashed_password) if hashed_password is not None else None,
            salt=Salt(salt) if salt is not None else None,
            role_id=dto.role_id
        )
