#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import AsyncIterable

from application.dtos import (
    FilesListDto,
    FileContentDto,
    FilesGetListDto,
    FileGetContentDto,
    FilesMoveDto,
    FileRenameDto,
    FilesDuplicateDto,
    FilesDeleteDto,
    FilesDownloadDto,
    FileSaveContentDto,
    FileCreateDto,
    FilesUploadDto,
    FilesExtractDto
)


class AbstractFilesService(ABC):
    """
    Abstract files service.
    """

    @abstractmethod
    async def get_list(
        self,
        server_id: int,
        dto: FilesGetListDto
    ) -> FilesListDto:
        """
        Gets a list of files in the given directory.

        Parameters:
        - server_id: Server ID.
        - dto: FilesGetListDto object.

        Returns:
        - FilesListDto: FilesListDto object.
        """
        ...

    @abstractmethod
    async def get_content(
        self,
        server_id: int,
        dto: FileGetContentDto
    ) -> FileContentDto:
        """
        Gets the content of a file.

        Parameters:
        - server_id: Server ID.
        - dto: FileGetContentDto object.

        Returns:
        - FileContentDto: FileContentDto object.
        """
        ...

    @abstractmethod
    async def save_content(
        self,
        server_id: int,
        dto: FileSaveContentDto
    ) -> None:
        """
        Saves the content of a file.

        Parameters:
        - server_id: Server ID.
        - dto: FileSaveContentDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def create(
        self,
        server_id: int,
        dto: FileCreateDto
    ) -> None:
        """
        Creates a new file.

        Parameters:
        - server_id: Server ID.
        - dto: FileCreateDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def upload(
        self,
        server_id: int,
        dto: FilesUploadDto
    ) -> None:
        """
        Uploads one or multiple files to the given directory.

        Parameters:
        - server_id: Server ID.
        - dto: FilesUploadDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def download(
        self,
        server_id: int,
        dto: FilesDownloadDto
    ) -> AsyncIterable[bytes]:
        """
        Streams one or multiple files/directories as a zip archive.

        Parameters:
        - server_id: Server ID.
        - dto: FilesDownloadDto object.

        Returns:
        - AsyncIterable: Zip archive byte chunks.
        """
        ...

    @abstractmethod
    async def move(
        self,
        server_id: int,
        dto: FilesMoveDto
    ) -> None:
        """
        Moves one or multiple files/directories to the destination path.

        Parameters:
        - server_id: Server ID.
        - dto: FilesMoveDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def rename(
        self,
        server_id: int,
        dto: FileRenameDto
    ) -> None:
        """
        Renames a file or directory.

        Parameters:
        - server_id: Server ID.
        - dto: FileRenameDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def duplicate(
        self,
        server_id: int,
        dto: FilesDuplicateDto
    ) -> None:
        """
        Duplicates one or multiple files/directories.

        Parameters:
        - server_id: Server ID.
        - dto: FilesDuplicateDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def extract(
        self,
        server_id: int,
        dto: FilesExtractDto
    ) -> None:
        """
        Extracts a ZIP archive to the destination path.

        Parameters:
        - server_id: Server ID.
        - dto: FilesExtractDto object.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def delete(
        self,
        server_id: int,
        dto: FilesDeleteDto
    ) -> None:
        """
        Deletes one or multiple files/directories.

        Parameters:
        - server_id: Server ID.
        - dto: FilesDeleteDto object.

        Returns:
        - None.
        """
        ...