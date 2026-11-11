#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
Factories for building domain entities and application DTOs in tests.
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from typing import List, Optional

from domain.enums import (
    PermissionEnum,
    LanguageEnum,
    ThemeEnum,
    TimezoneEnum,
    ServerStateEnum,
    FileTypeEnum
)
from domain.value_objects import (
    RoleName,
    Login,
    HashedPassword,
    Salt,
    AttributeKey,
    GameName,
    LoaderName,
    LoaderVersion,
    ServerName
)
from domain.entities import (
    AttributeEntity,
    GameEntity,
    LoaderEntity,
    ServerEntity,
    RoleEntity,
    RolesPageEntity,
    SettingsEntity,
    UserEntity,
    UsersPageEntity
)
from application.dtos import (
    AttributeDto,
    FileDto,
    GameDto,
    LoaderDto,
    MetricDto,
    RoleDto,
    ServerDto,
    SettingsDto,
    UserDto
)


NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def make_role_entity(
    role_id: int = 1,
    name: str = "admin",
    permissions: Optional[List[PermissionEnum]] = None
) -> RoleEntity:
    return RoleEntity(
        id=role_id,
        name=RoleName(name),
        permissions=permissions if permissions is not None else [PermissionEnum.ROLES_VIEW],
        created_at=NOW,
        updated_at=NOW
    )


def make_roles_page_entity(
    roles: Optional[List[RoleEntity]] = None,
    page: int = 1
) -> RolesPageEntity:
    roles = roles if roles is not None else [make_role_entity()]

    return RolesPageEntity(
        roles=roles,
        total=len(roles),
        page=page,
        pages=1
    )


def make_settings_entity(
    user_id: int = 1,
    language: LanguageEnum = LanguageEnum.EN
) -> SettingsEntity:
    return SettingsEntity(
        id=user_id,
        user_id=user_id,
        language=language,
        theme=ThemeEnum.COBALT_DARK,
        timezone=TimezoneEnum.UTC_MINUS_8,
        created_at=NOW,
        updated_at=NOW
    )


def make_user_entity(
    user_id: int = 1,
    login: str = "john_doe",
    role: Optional[RoleEntity] = None
) -> UserEntity:
    return UserEntity(
        id=user_id,
        login=Login(login),
        hashed_password=HashedPassword("hashed"),
        salt=Salt("salt"),
        role=role if role is not None else make_role_entity(),
        settings=make_settings_entity(user_id=user_id),
        created_at=NOW,
        updated_at=NOW
    )


def make_users_page_entity(
    users: Optional[List[UserEntity]] = None
) -> UsersPageEntity:
    users = users if users is not None else [make_user_entity()]

    return UsersPageEntity(
        users=users,
        total=len(users),
        page=1,
        pages=1
    )


def make_role_dto(
    role_id: int = 1,
    name: str = "admin",
    permissions: Optional[List[PermissionEnum]] = None
) -> RoleDto:
    return RoleDto(
        id=role_id,
        name=name,
        permissions=permissions if permissions is not None else list(PermissionEnum),
        created_at=NOW,
        updated_at=NOW
    )


def make_settings_dto(
    user_id: int = 1,
    language: LanguageEnum = LanguageEnum.EN
) -> SettingsDto:
    return SettingsDto(
        id=user_id,
        user_id=user_id,
        language=language,
        theme=ThemeEnum.COBALT_DARK,
        timezone=TimezoneEnum.UTC_MINUS_8,
        created_at=NOW,
        updated_at=NOW
    )


def make_user_dto(
    user_id: int = 1,
    login: str = "john_doe",
    role: Optional[RoleDto] = None,
    language: LanguageEnum = LanguageEnum.EN
) -> UserDto:
    return UserDto(
        id=user_id,
        login=login,
        hashed_password="hashed",
        salt="salt",
        role=role if role is not None else make_role_dto(),
        settings=make_settings_dto(user_id=user_id, language=language),
        created_at=NOW,
        updated_at=NOW
    )


def make_loader_dto(
    loader_id: int = 1,
    game_id: int = 1,
    name: str = "vanilla"
) -> LoaderDto:
    return LoaderDto(
        id=loader_id,
        game_id=game_id,
        name=name,
        versions=["1.0.0", "1.1.0"],
        created_at=NOW,
        updated_at=NOW
    )


def make_game_dto(
    game_id: int = 1,
    name: str = "minecraft"
) -> GameDto:
    return GameDto(
        id=game_id,
        name=name,
        loaders=[make_loader_dto(game_id=game_id)],
        created_at=NOW,
        updated_at=NOW
    )


def make_attribute_dto(
    attribute_id: int = 1,
    server_id: int = 1,
    key: str = "max_players",
    value: str = "10"
) -> AttributeDto:
    return AttributeDto(
        id=attribute_id,
        server_id=server_id,
        key=key,
        value=value,
        created_at=NOW,
        updated_at=NOW
    )


def make_server_dto(
    server_id: int = 1,
    name: str = "survival",
    state: ServerStateEnum = ServerStateEnum.INSTALLED
) -> ServerDto:
    return ServerDto(
        id=server_id,
        name=name,
        version="1.0.0",
        game=make_game_dto(),
        loader=make_loader_dto(),
        attributes=[make_attribute_dto(server_id=server_id)],
        state=state,
        created_at=NOW,
        updated_at=NOW
    )


def make_metric_dto(
    value: float = 42.5
) -> MetricDto:
    return MetricDto(
        value=value,
        date=NOW
    )


def make_file_dto(
    name: str = "server.properties",
    path: str = "/server.properties",
    file_type: FileTypeEnum = FileTypeEnum.FILE
) -> FileDto:
    return FileDto(
        name=name,
        path=path,
        type=file_type,
        format="properties" if file_type == FileTypeEnum.FILE else None,
        size=128 if file_type == FileTypeEnum.FILE else None,
        modified_at=NOW
    )


def make_loader_entity(
    loader_id: int = 1,
    game_id: int = 1,
    name: str = "vanilla",
    versions: Optional[List[str]] = None
) -> LoaderEntity:
    return LoaderEntity(
        id=loader_id,
        game_id=game_id,
        name=LoaderName(name),
        versions=[LoaderVersion(v) for v in (versions if versions is not None else ["1.2.0", "1.1.0", "1.0.0"])],
        created_at=NOW,
        updated_at=NOW
    )


def make_game_entity(
    game_id: int = 1,
    name: str = "minecraft"
) -> GameEntity:
    return GameEntity(
        id=game_id,
        name=GameName(name),
        loaders=[make_loader_entity(game_id=game_id)],
        created_at=NOW,
        updated_at=NOW
    )


def make_server_entity(
    server_id: int = 1,
    state: ServerStateEnum = ServerStateEnum.INSTALLED,
    version: str = "1.0.0",
    game_name: str = "minecraft",
    loader_name: str = "vanilla"
) -> ServerEntity:
    return ServerEntity(
        id=server_id,
        name=ServerName("survival"),
        version=LoaderVersion(version),
        game=make_game_entity(name=game_name),
        loader=make_loader_entity(name=loader_name),
        attributes=[
            AttributeEntity(
                id=1, server_id=server_id, key=AttributeKey("max_players"), value="10",
                created_at=NOW, updated_at=NOW
            )
        ],
        state=state,
        created_at=NOW,
        updated_at=NOW
    )


def make_connection(
    user: UserDto
) -> SimpleNamespace:
    """
    Builds a minimal WebSocket connection stub exposing `state.user`.
    """
    return SimpleNamespace(
        state=SimpleNamespace(
            user=user
        )
    )
