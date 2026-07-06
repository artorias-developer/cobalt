#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any

from structlog import BoundLogger

from application.contracts.loggers import AbstractLogger


class StructlogLogger(AbstractLogger):
    """
    Structlog logger.
    """

    def __init__(
        self,
        logger: BoundLogger
    ):
        super().__init__(logger)

    def debug(self, message: str, **kwargs: Any) -> None:
        """
        Writes debug message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        self.logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """
        Writes info message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """
        Writes warning message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        self.logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """
        Writes error message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        self.logger.error(message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """
        Writes critical message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        self.logger.critical(message, **kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        """
        Writes exception message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        self.logger.exception(message, **kwargs)