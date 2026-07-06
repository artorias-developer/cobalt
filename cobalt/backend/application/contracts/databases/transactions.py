#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from application.contracts.loggers import AbstractLogger


AbstractRepository = TypeVar("AbstractRepository")


class AbstractTransaction(ABC):
    """
    Abstract class for database transaction.
    """
    session: Any

    logger: AbstractLogger

    def __init__(
        self,
        logger: AbstractLogger
    ):
        self.logger = logger

        self.session = None

    @abstractmethod
    async def __aenter__(self) -> "AbstractTransaction":
        """
        Starts the transaction.

        Parameters:
        - None.

        Returns:
        - AbstractTransaction: Current transaction instance.
        """
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Commits or rolls back the transaction.

        Parameters:
        - exc_type: Exception type.
        - exc_val: Exception value.
        - exc_tb: Exception traceback.

        Returns:
        - None.
        """
        ...
