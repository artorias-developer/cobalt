#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path

from domain.enums import LanguageEnum
from infrastructure.configs.application.enums import EnvironmentEnum


@dataclass(slots=True)
class ServerSettings:
    host: str
    port: int
    domain: str
    root_dir: Path
    host_containers_dir: Path
    app_containers_dir: Path
    environment: EnvironmentEnum

@dataclass(slots=True)
class LoggerSettings:
    logger_name: str
    format: str
    date_fmt: str
    max_size: int
    backup_count: int
    log_dir: Path
    log_file: str

@dataclass(slots=True)
class DatabaseSettings:
    url: str
    pool_size: int
    pool_recycle: int
    pool_timeout: int
    pool_pre_ping: bool
    echo: bool
    expire_on_commit: bool

@dataclass(slots=True)
class RedisSettings:
    url: str

@dataclass(slots=True)
class PrometheusSettings:
    url: str

@dataclass(slots=True)
class SecuritySettings:
    pepper: str
    bcrypt_rounds: int

@dataclass(slots=True)
class I18nSettings:
    locales_dir: Path
    domain: str
    default_language: LanguageEnum

@dataclass(slots=True)
class ApplicationConfig:
    server: ServerSettings
    database: DatabaseSettings
    redis: RedisSettings
    prometheus: PrometheusSettings
    logging: LoggerSettings
    security: SecuritySettings
    i18n: I18nSettings