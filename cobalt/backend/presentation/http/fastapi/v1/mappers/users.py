#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.dtos import (
    UserDto,
    UsersGetPageDto,
    UsersPageDto,
    UserCreateDto,
    UserUpdateDto
)
from presentation.contracts.http.mappers import (
    AbstractUsersRouterMapper,
    AbstractRolesRouterMapper,
    AbstractSettingsRouterMapper
)
from presentation.http.fastapi.v1.schemas import (
    UserSchema,
    UserMeSchema,
    UsersGetPageSchema,
    UsersPageSchema,
    UserCreateSchema,
    UserUpdateSchema
)


class UsersRouterMapper(AbstractUsersRouterMapper):
    """
    Mapper for users router.
    """
    roles_mapper: AbstractRolesRouterMapper
    settings_mapper: AbstractSettingsRouterMapper

    def __init__(
        self,
        roles_mapper: AbstractRolesRouterMapper,
        settings_mapper: AbstractSettingsRouterMapper
    ):
        self.roles_mapper = roles_mapper
        self.settings_mapper = settings_mapper

    def dto_to_schema(
        self,
        dto: UserDto
    ) -> UserSchema:
        """
        Converts UserDto object to UserSchema object.

        Parameters:
        - dto: UserDto object.

        Returns:
        - UserSchema: UserSchema object.
        """
        return UserSchema(
            id=dto.id,
            login=dto.login,
            role=self.roles_mapper.dto_to_schema(
                dto=dto.role
            ),
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    def dtos_to_schemas(
        self,
        dtos: List[UserDto]
    ) -> List[UserSchema]:
        """
        Converts UserDto objects to UserSchema objects.

        Parameters:
        - dtos: List of UserDto objects.

        Returns:
        - List: List of UserSchema objects.
        """
        return [
            self.dto_to_schema(dto)
            for dto in dtos
        ]

    def page_dto_to_schema(
        self,
        dto: UsersPageDto
    ) -> UsersPageSchema:
        """
        Converts UsersPageDto object to UsersPageSchema object.

        Parameters:
        - dto: UsersPageDto object.

        Returns:
        - UsersPageSchema: UsersPageSchema object.
        """
        return UsersPageSchema(
            users=self.dtos_to_schemas(
                dtos=dto.users
            ),
            total=dto.total,
            page=dto.page,
            pages=dto.pages
        )

    def get_page_schema_to_dto(
        self,
        schema: UsersGetPageSchema
    ) -> UsersGetPageDto:
        """
        Converts UsersGetPageSchema object to UsersGetPageDto object.

        Parameters:
        - schema: UsersGetPageSchema object.

        Returns:
        - UsersGetPageDto: UsersGetPageDto object.
        """
        return UsersGetPageDto(
            page=schema.page,
            search=schema.search,
            sort_field=schema.sort_field,
            sort_direction=schema.sort_direction,
            limit=schema.limit
        )

    def dto_to_me_schema(
        self,
        dto: UserDto
    ) -> UserMeSchema:
        """
        Converts UserDto object to UserMeSchema object.

        Parameters:
        - dto: UserDto object.

        Returns:
        - UserMeSchema: UserMeSchema object.
        """
        return UserMeSchema(
            id=dto.id,
            login=dto.login,
            role=self.roles_mapper.dto_to_schema(
                dto=dto.role
            ),
            settings=self.settings_mapper.dto_to_schema(
                dto=dto.settings
            ),
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    def create_schema_to_dto(
        self,
        schema: UserCreateSchema
    ) -> UserCreateDto:
        """
        Converts UserCreateSchema object to UserCreateDto object.

        Parameters:
        - schema: UserCreateSchema object.

        Returns:
        - UserCreateDto: UserCreateDto object.
        """
        return UserCreateDto(
            login=schema.login,
            password=schema.password,
            role_id=schema.role_id
        )

    def update_schema_to_dto(
        self,
        schema: UserUpdateSchema
    ) -> UserUpdateDto:
        """
        Converts UserUpdateSchema object to UserUpdateDto object.

        Parameters:
        - schema: UserUpdateSchema object.

        Returns:
        - UserUpdateDto: UserUpdateDto object.
        """
        return UserUpdateDto(
            login=schema.login,
            password=schema.password,
            role_id=schema.role_id
        )
