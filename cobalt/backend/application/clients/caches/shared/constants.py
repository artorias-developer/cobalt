#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

class CacheConstants:
    """
    Cache-related constants.
    """
    SHORT_TTL_SECONDS: int = 5 * 60
    NORMAL_TTL_SECONDS: int = 1 * 60 * 60
    LONG_TTL_SECONDS: int = 24 * 60 * 60

    USERS_PAGE_KEY: str = "users:page:{page}:{search}:{sort_field}:{sort_direction}:{limit}"
    USERS_ITEM_KEY: str = "users:item:{user_id}:{login}:{role_id}"

    ROLES_PAGE_KEY: str = "roles:page:{page}:{search}:{sort_field}:{sort_direction}:{limit}"
    ROLES_ITEM_KEY: str = "roles:item:{role_id}"

    LOADERS_ITEM_KEY: str = "loaders:item:{loader_id}:{name}:{game_id}"

    GAMES_PAGE_KEY: str = "games:page:{page}:{search}:{sort_field}:{sort_direction}:{limit}"
    GAMES_ITEM_KEY: str = "games:item:{game_id}:{name}"

    SERVERS_PAGE_KEY: str = "servers:page:{page}:{search}:{sort_field}:{sort_direction}:{limit}"
    SERVERS_ITEM_KEY: str = "servers:item:{server_id}:{game_id}:{loader_id}"

    ATTRIBUTES_PAGE_KEY: str = "attributes:page:{server_id}:{page}:{search}:{sort_field}:{sort_direction}:{limit}"
    ATTRIBUTES_ITEM_KEY: str = "attributes:item:{attribute_id}:{key}:{server_id}"

    METRICS_HOST_DISK_KEY: str = "metrics:host:disk"

    SETTINGS_ITEM_KEY: str = "settings:item:{user_id}"

    SESSION_KEY: str = "session:{session_id}"