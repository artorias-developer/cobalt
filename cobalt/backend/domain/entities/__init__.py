#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .attributes import (
    AttributeEntity,
    AttributesPageEntity,
    AttributesGetPageEntity,
    AttributeCreateEntity,
    AttributeUpdateEntity
)
from .games import (
    GameEntity,
    GamesPageEntity,
    GamesGetPageEntity,
    GameCreateEntity,
    GameUpdateEntity
)
from .loaders import (
    LoaderEntity,
    LoaderCreateEntity,
    LoaderUpdateEntity
)
from .roles import (
    RoleEntity,
    RolesPageEntity,
    RolesGetPageEntity,
    RoleCreateEntity,
    RoleUpdateEntity
)
from .servers import (
    ServerEntity,
    ServersPageEntity,
    ServersGetPageEntity,
    ServerCreateEntity,
    ServerUpdateEntity
)
from .settings import (
    SettingsEntity,
    SettingsUpdateEntity
)
from .users import (
    UserEntity,
    UsersPageEntity,
    UsersGetPageEntity,
    UserCreateEntity,
    UserUpdateEntity
)

__all__ = [
    "AttributeEntity",
    "AttributesPageEntity",
    "AttributesGetPageEntity",
    "AttributeCreateEntity",
    "AttributeUpdateEntity",
    "GameEntity",
    "GamesPageEntity",
    "GamesGetPageEntity",
    "GameCreateEntity",
    "GameUpdateEntity",
    "LoaderEntity",
    "LoaderCreateEntity",
    "LoaderUpdateEntity",
    "RoleEntity",
    "RolesPageEntity",
    "RolesGetPageEntity",
    "RoleCreateEntity",
    "RoleUpdateEntity",
    "ServerEntity",
    "ServersPageEntity",
    "ServersGetPageEntity",
    "ServerCreateEntity",
    "ServerUpdateEntity",
    "SettingsEntity",
    "SettingsUpdateEntity",
    "UserEntity",
    "UsersPageEntity",
    "UsersGetPageEntity",
    "UserCreateEntity",
    "UserUpdateEntity"
]
