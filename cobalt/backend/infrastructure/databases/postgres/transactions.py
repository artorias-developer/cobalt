#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from application.contracts.databases import AbstractTransaction
from application.contracts.loggers import AbstractLogger


class Transaction(AbstractTransaction):
    """
    Transaction for Postgres repositories.
    """
    session: Optional[AsyncSession]

    session_factory: async_sessionmaker
    logger: AbstractLogger

    def __init__(
        self,
        session_factory: async_sessionmaker,
        logger: AbstractLogger
    ):
        """
        Initializes the transaction manager.

        Parameters:
        - session_factory: SQLAlchemy async session factory.
        - logger: Application logger instance.

        Returns:
        - None.
        """
        super().__init__(logger)

        self.session_factory = session_factory
        self.logger = logger

    async def __aenter__(self) -> "Transaction":
        """
        Starts a new database transaction.

        Parameters:
        - None.

        Returns:
        - Transaction: Current transaction instance.
        """
        self._session = self.session_factory()

        return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ) -> None:
        """
        Commits or rolls back the transaction.

        Parameters:
        - exc_type: Exception type.
        - exc_val: Exception value.
        - exc_tb: Exception traceback.

        Returns:
        - None.
        """
        if self._session is None:
            return

        try:
            if exc_type is not None:
                await self._session.rollback()
            else:
                await self._session.commit()

        except Exception:
            self.logger.exception("Transaction finalization failed:")

            raise

        finally:
            await self._session.close()
            self._session = None