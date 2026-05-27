#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any


class AbstractLogger(ABC):
    """
    Abstract logger.
    """
    logger: Any

    def __init__(
        self,
        logger: Any
    ):
        self.logger = logger

    @abstractmethod
    def debug(
        self,
        message: str,
        **kwargs: Any
    ) -> None:
        """
        Writes debug message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def info(
        self,
        message: str,
        **kwargs: Any
    ) -> None:
        """
        Writes info message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def warning(
        self,
        message: str,
        **kwargs: Any
    ) -> None:
        """
        Writes warning message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def error(
        self,
        message: str,
        **kwargs: Any
    ) -> None:
        """
        Writes error message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def critical(
        self,
        message: str,
        **kwargs: Any
    ) -> None:
        """
        Writes critical message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def exception(
        self,
        message: str,
        **kwargs: Any
    ) -> None:
        """
        Writes exception message.

        Parameters:
        - message: Message to write.
        - kwargs: Keyword arguments.

        Returns:
        - None.
        """
        ...
