#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy.ext.asyncio import async_sessionmaker

from application.contracts.databases import AbstractTransactionsManager
from application.contracts.loggers import AbstractLogger
from infrastructure.databases.postgres.transactions import TransactionsManager


def create_postgres_transactions_manager(
    session_factory: async_sessionmaker,
    logger: AbstractLogger
) -> AbstractTransactionsManager:
    """
    Creates a Postgres transactions manager.

    Parameters:
    - session_factory: async_sessionmaker object.
    - logger: AbstractLogger object.

    Returns:
    - Transaction: Transaction object.
    """
    return TransactionsManager(
        session_factory=session_factory,
        logger=logger
    )