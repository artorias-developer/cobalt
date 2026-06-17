#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from application.contracts.loggers import AbstractLogger
from infrastructure.configs import ApplicationConfig
from composition.dataclasses import (
    DatabaseContainer,
    MappersContainer,
    ManagersContainer
)

from .repositories import create_postgres_repositories
from .transactions import create_postgres_transactions_manager

__all__ = [
    "create_postgres_database_container"
]


def create_postgres_database_container(
    config: ApplicationConfig,
    managers: ManagersContainer,
    mappers: MappersContainer,
    logger: AbstractLogger
) -> DatabaseContainer:
    """
    Creates a Postgres database container.

    Parameters:
    - config: ApplicationConfig object.
    - managers: ManagersContainer object.
    - mappers: MappersContainer object.
    - logger: AbstractLogger object.

    Returns:
    - DatabaseContainer: DatabaseContainer object.
    """
    engine = create_async_engine(
        url=config.database.url,
        pool_size=config.database.pool_size,
        pool_recycle=config.database.pool_recycle,
        pool_timeout=config.database.pool_timeout,
        pool_pre_ping=config.database.pool_pre_ping,
        echo=False
    )

    session_factory = async_sessionmaker(
        bind=engine,
        expire_on_commit=config.database.expire_on_commit,
        class_=AsyncSession,
        autobegin=True
    )

    created_repositories = create_postgres_repositories(
        session_factory=session_factory,
        managers=managers,
        mappers=mappers.repositories,
        logger=logger
    )

    created_transactions_manager = create_postgres_transactions_manager(
        session_factory=session_factory,
        logger=logger
    )

    return DatabaseContainer(
        repositories=created_repositories,
        transactions_manager=created_transactions_manager
    )