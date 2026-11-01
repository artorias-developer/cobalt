#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import getenv
from pathlib import Path

from domain.enums import (
    LanguageEnum,
    EnvironmentEnum
)
from infrastructure.configs.application.dataclasses import (
    ApplicationConfig,
    ServerSettings,
    LoggerSettings,
    DatabaseSettings,
    RedisSettings,
    PrometheusSettings,
    SecuritySettings,
    I18nSettings,
    ContainersSettings
)


def get_application_config() -> ApplicationConfig:
    """
    Gets application config.

    Parameters:
    - None.

    Returns:
    - ApplicationConfig: ApplicationConfig object.
    """
    database_url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
        user=getenv("POSTGRES_USER"),
        password=getenv("POSTGRES_PASSWORD"),
        host=getenv("POSTGRES_HOST"),
        port=getenv("POSTGRES_PORT"),
        db=getenv("POSTGRES_DB")
    )

    redis_url = "redis://:{password}@{host}:{port}/{db}".format(
        password=getenv("REDIS_PASSWORD"),
        host=getenv("REDIS_HOST"),
        port=getenv("REDIS_PORT"),
        db=getenv("REDIS_DB")
    )

    prometheus_url = "http://{host}:{port}".format(
        host=getenv("PROMETHEUS_HOST"),
        port=getenv("PROMETHEUS_PORT")
    )

    if getenv("APP_ENVIRONMENT") == "dev":
        environment = EnvironmentEnum.DEVELOPMENT
    else:
        environment = EnvironmentEnum.PRODUCTION

    generated_dir = Path(__file__).parents[5] / "generated" / "backend"

    server = ServerSettings(
        host=getenv("BACKEND_HOST"),
        port=int(getenv("BACKEND_PORT")),
        domain=getenv("APP_DOMAIN"),
        host_containers_dir=Path(getenv("HOST_CONTAINERS_ROOT")),
        app_containers_dir=generated_dir / "containers",
        environment=environment
    )

    database = DatabaseSettings(
        url=database_url,
        pool_size=int(getenv("POSTGRES_POOL_SIZE")),
        pool_recycle=int(getenv("POSTGRES_POOL_RECYCLE")),
        pool_timeout=int(getenv("POSTGRES_POOL_TIMEOUT")),
        pool_pre_ping=getenv("POSTGRES_POOL_PRE_PING") == "1",
        echo=getenv("POSTGRES_ECHO") == "1",
        expire_on_commit=getenv("POSTGRES_EXPIRE_ON_COMMIT") == "1"
    )

    redis = RedisSettings(
        url=redis_url
    )

    prometheus = PrometheusSettings(
        url=prometheus_url
    )

    security = SecuritySettings(
        pepper=getenv("APP_PEPPER"),
        bcrypt_rounds=int(getenv("APP_BCRYPT_ROUNDS"))
    )

    logging = LoggerSettings(
        logger_name=getenv("LOGGER_NAME"),
        format=getenv("LOGGER_FORMAT"),
        date_fmt=getenv("LOGGER_DATE_FMT"),
        max_size=int(getenv("LOGGER_MAX_SIZE")),
        backup_count=int(getenv("LOGGER_BACKUP_COUNT")),
        log_dir=generated_dir / "logs",
        log_file=getenv("LOGGER_FILE")
    )

    i18n = I18nSettings(
        locales_dir=Path(__file__).parents[3] / "infrastructure" / "locales" / "babel",
        domain="messages",
        default_language=LanguageEnum.EN
    )

    containers = ContainersSettings(
        socket_path=getenv("CONTAINERS_SOCKET_PATH"),
        base_url=getenv("CONTAINERS_BASE_URL"),
        cli_path=getenv("CONTAINERS_CLI_PATH")
    )

    return ApplicationConfig(
        server=server,
        database=database,
        redis=redis,
        prometheus=prometheus,
        containers=containers,
        logging=logging,
        security=security,
        i18n=i18n
    )
