#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import Any

from presentation.contracts.http.routers import AbstractHttpRouter


class AbstractHttpFilesRouter(AbstractHttpRouter, ABC):
    """
    Abstract HTTP router for server files operations.
    """

    @abstractmethod
    async def get_list(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets a list of files in the given directory.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def get_content(self, *args: Any, **kwargs: Any) -> Any:
        """
        Gets the content of a specific file.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def save_content(self, *args: Any, **kwargs: Any) -> Any:
        """
        Saves the content of a specific file.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def create(self, *args: Any, **kwargs: Any) -> Any:
        """
        Creates a new file.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def upload(self, *args: Any, **kwargs: Any) -> Any:
        """
        Uploads one or multiple files to the given directory.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def download(self, *args: Any, **kwargs: Any) -> Any:
        """
        Downloads one or multiple files/directories as a zip archive.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def move(self, *args: Any, **kwargs: Any) -> Any:
        """
        Moves one or multiple files/directories to the destination path.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def rename(self, *args: Any, **kwargs: Any) -> Any:
        """
        Renames a file or directory.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def duplicate(self, *args: Any, **kwargs: Any) -> Any:
        """
        Duplicates one or multiple files/directories.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def extract(self, *args: Any, **kwargs: Any) -> Any:
        """
        Extracts a ZIP archive to the destination path.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...

    @abstractmethod
    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        """
        Deletes one or multiple files/directories.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - Any: Response object.
        """
        ...