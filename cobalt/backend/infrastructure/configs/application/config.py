#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import getenv
from pathlib import Path

from domain.enums import LanguageEnum
from infrastructure.configs.application.dataclasses import (
    ApplicationConfig,
    ServerSettings,
    LoggerSettings,
    DatabaseSettings,
    RedisSettings,
    PrometheusSettings,
    SecuritySettings,
    I18nSettings
)
from infrastructure.configs.application.enums import EnvironmentEnum


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

    server = ServerSettings(
        host=getenv("BACKEND_HOST"),
        port=int(getenv("BACKEND_PORT")),
        domain=getenv("APP_DOMAIN"),
        root_dir=Path(__file__).parents[1],
        host_containers_dir=Path(getenv("HOST_CONTAINERS_ROOT")),
        app_containers_dir=Path(__file__).parents[3] / "generated" / "containers",
        environment=environment
    )

    database = DatabaseSettings(
        url=database_url,
        pool_size=30,
        pool_recycle=300,
        pool_timeout=30,
        pool_pre_ping=True,
        echo=False,
        expire_on_commit=False
    )

    redis = RedisSettings(
        url=redis_url
    )

    prometheus = PrometheusSettings(
        url=prometheus_url
    )

    security = SecuritySettings(
        global_salt=getenv("APP_GLOBAL_SALT"),
        bcrypt_rounds=int(getenv("APP_BCRYPT_ROUNDS"))
    )

    logging = LoggerSettings(
        logger_name="cobalt.app",
        format="%(asctime)s %(levelname)s %(message)s",
        date_fmt="%Y-%m-%d %H:%M:%S",
        max_size=10 * 1024 * 1024,
        backup_count=1,
        log_dir=Path(__file__).parents[3] / "logs",
        log_file="cobalt.log"
    )

    i18n = I18nSettings(
        locales_dir=Path(__file__).parents[3] / "infrastructure" / "locales",
        domain="messages",
        default_language=LanguageEnum.EN
    )

    return ApplicationConfig(
        server=server,
        database=database,
        redis=redis,
        prometheus=prometheus,
        logging=logging,
        security=security,
        i18n=i18n
    )
