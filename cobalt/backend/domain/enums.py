#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from enum import StrEnum


class PermissionsEnum(StrEnum):
    """
    User permissions enum.
    """
    DASHBOARD_VIEW = "dashboard_view"
    DASHBOARD_CPU_VIEW = "dashboard_cpu_view"
    DASHBOARD_RAM_VIEW = "dashboard_ram_view"
    DASHBOARD_DISK_VIEW = "dashboard_disk_view"
    DASHBOARD_LOGS_VIEW = "dashboard_logs_view"
    SERVERS_VIEW = "servers_view"
    SERVERS_CREATE = "servers_create"
    SERVERS_DELETE = "servers_delete"
    SERVER_VIEW = "server_view"
    SERVER_UPDATE = "server_update"
    SERVER_START = "server_start"
    SERVER_STOP = "server_stop"
    SERVER_CPU_VIEW = "server_cpu_view"
    SERVER_RAM_VIEW = "server_ram_view"
    SERVER_LOGS_VIEW = "server_logs_view"
    SERVER_CONSOLE_EXECUTE = "server_console_execute"
    SERVER_FILES_VIEW = "server_files_view"
    SERVER_FILES_UPDATE = "server_files_update"
    SERVER_FILES_DOWNLOAD = "server_files_download"
    SERVER_SETTINGS_VIEW = "server_settings_view"
    SERVER_SETTINGS_UPDATE = "server_settings_update"
    USERS_VIEW = "users_view"
    USERS_CREATE = "users_create"
    USERS_UPDATE = "users_update"
    USERS_DELETE = "users_delete"
    ROLES_VIEW = "roles_view"
    ROLES_CREATE = "roles_create"
    ROLES_UPDATE = "roles_update"
    ROLES_DELETE = "roles_delete"
    GAMES_VIEW = "games_view"
    SETTINGS_CACHE_CLEAR = "settings_cache_clear"
    SETTINGS_CONTAINERS_CLEAR = "settings_containers_clear"

class ServerStatusEnum(StrEnum):
    """
    Server status enum.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    CREATED = "created"
    FAILED = "failed"

class LanguageEnum(StrEnum):
    """
    Language enum.
    """
    EN = "en"

class ThemeEnum(StrEnum):
    """
    Theme enum.
    """
    DARK = "dark"

class TimezoneEnum(StrEnum):
    """
    Timezone enum.
    """
    UTC_MINUS_12 = "UTC-12"
    UTC_MINUS_11 = "UTC-11"
    UTC_MINUS_10 = "UTC-10"
    UTC_MINUS_9 = "UTC-9"
    UTC_MINUS_8 = "UTC-8"
    UTC_MINUS_7 = "UTC-7"
    UTC_MINUS_6 = "UTC-6"
    UTC_MINUS_5 = "UTC-5"
    UTC_MINUS_4 = "UTC-4"
    UTC_MINUS_3 = "UTC-3"
    UTC_MINUS_2 = "UTC-2"
    UTC_MINUS_1 = "UTC-1"
    UTC = "UTC"
    UTC_PLUS_1 = "UTC+1"
    UTC_PLUS_2 = "UTC+2"
    UTC_PLUS_3 = "UTC+3"
    UTC_PLUS_4 = "UTC+4"
    UTC_PLUS_5 = "UTC+5"
    UTC_PLUS_6 = "UTC+6"
    UTC_PLUS_7 = "UTC+7"
    UTC_PLUS_8 = "UTC+8"
    UTC_PLUS_9 = "UTC+9"
    UTC_PLUS_10 = "UTC+10"
    UTC_PLUS_11 = "UTC+11"
    UTC_PLUS_12 = "UTC+12"
