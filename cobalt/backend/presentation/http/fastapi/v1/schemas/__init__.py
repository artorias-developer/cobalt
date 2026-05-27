#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .attributes import (
    AttributeSchema,
    AttributesGetPageSchema,
    AttributesPageSchema,
    AttributeCreateSchema,
    AttributeUpdateSchema,
    AttributesUpdateSchema,
    AttributesDeleteSchema
)
from .auth import (
    AuthLoginSchema,
    AuthChangeCredentialsSchema
)
from .files import (
    FileSchema,
    FilesGetListSchema,
    FilesListSchema,
    FileGetContentSchema,
    FileContentSchema,
    FilesMoveSchema,
    FilesDuplicateSchema,
    FilesDeleteSchema,
    FilesDownloadSchema,
    FileRenameSchema,
    FileSaveContentSchema,
    FileCreateSchema,
    FilesExtractSchema
)
from .games import (
    GameSchema,
    GameShortSchema,
    GamesGetPageSchema,
    GamesPageSchema
)
from .loaders import (
    LoaderSchema,
    LoaderShortSchema
)
from .logs import LogSchema
from .metrics import (
    MetricSchema,
    MetricDiskSchema
)
from .users import (
    UserSchema,
    UserMeSchema,
    UsersGetPageSchema,
    UsersPageSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UsersDeleteSchema
)
from .servers import (
    ServerSchema,
    ServersGetPageSchema,
    ServersPageSchema,
    ServerCreateSchema,
    ServerUpdateSchema,
    ServersDeleteSchema,
    ServerExecuteSchema,
    ServerStatusSchema
)
from .settings import (
    SettingsSchema,
    SettingsUpdateSchema
)
from .roles import (
    RoleSchema,
    RolesGetPageSchema,
    RolesPageSchema,
    RoleCreateSchema,
    RoleUpdateSchema,
    RolesDeleteSchema
)

__all__ = [
    "AttributeSchema",
    "AttributesGetPageSchema",
    "AttributesPageSchema",
    "AttributeCreateSchema",
    "AttributeUpdateSchema",
    "AttributesUpdateSchema",
    "AttributesDeleteSchema",
    "AuthLoginSchema",
    "AuthChangeCredentialsSchema",
    "FileSchema",
    "FilesGetListSchema",
    "FilesListSchema",
    "FileGetContentSchema",
    "FileContentSchema",
    "FilesMoveSchema",
    "FilesDuplicateSchema",
    "FilesDeleteSchema",
    "FilesDownloadSchema",
    "FileRenameSchema",
    "FileSaveContentSchema",
    "FileCreateSchema",
    "FilesExtractSchema",
    "GameSchema",
    "GameShortSchema",
    "GamesGetPageSchema",
    "GamesPageSchema",
    "LoaderSchema",
    "LoaderShortSchema",
    "LogSchema",
    "MetricSchema",
    "MetricDiskSchema",
    "UserSchema",
    "UserMeSchema",
    "UsersGetPageSchema",
    "UsersPageSchema",
    "UserCreateSchema",
    "UserUpdateSchema",
    "UsersDeleteSchema",
    "ServerSchema",
    "ServersGetPageSchema",
    "ServersPageSchema",
    "ServerCreateSchema",
    "ServerUpdateSchema",
    "ServersDeleteSchema",
    "ServerExecuteSchema",
    "ServerStatusSchema",
    "SettingsSchema",
    "SettingsUpdateSchema",
    "RoleSchema",
    "RolesGetPageSchema",
    "RolesPageSchema",
    "RoleCreateSchema",
    "RoleUpdateSchema",
    "RolesDeleteSchema"
]