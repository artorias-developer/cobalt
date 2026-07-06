#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any

from application.dtos import (
    FileDto,
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


class AbstractFilesRouterMapper(ABC):
    """
    Abstract mapper for files router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: FileDto
    ) -> Any:
        """
        Converts FileDto object to schema object.

        Parameters:
        - dto: FileDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def list_dto_to_schema(
        self,
        dto: FilesListDto
    ) -> Any:
        """
        Converts FilesListDto object to schema object.

        Parameters:
        - dto: FilesListDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def content_dto_to_schema(
        self,
        dto: FileContentDto
    ) -> Any:
        """
        Converts FileContentDto object to schema object.

        Parameters:
        - dto: FileContentDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def get_list_schema_to_dto(
        self,
        schema: Any
    ) -> FilesGetListDto:
        """
        Converts schema object to FilesGetListDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FilesGetListDto: FilesGetListDto object.
        """
        ...

    @abstractmethod
    def get_content_schema_to_dto(
        self,
        schema: Any
    ) -> FileGetContentDto:
        """
        Converts schema object to FileGetContentDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FileGetContentDto: FileGetContentDto object.
        """
        ...

    @abstractmethod
    def save_content_schema_to_dto(
        self,
        schema: Any
    ) -> FileSaveContentDto:
        """
        Converts schema object to FileSaveContentDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FileSaveContentDto: FileSaveContentDto object.
        """
        ...

    @abstractmethod
    def create_schema_to_dto(
        self,
        schema: Any
    ) -> FileCreateDto:
        """
        Converts schema object to FileCreateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FileCreateDto: FileCreateDto object.
        """
        ...

    @abstractmethod
    async def upload_schema_to_dto(
        self,
        path: str,
        files: Any
    ) -> FilesUploadDto:
        """
        Converts upload request parameters to FilesUploadDto object.

        Parameters:
        - path: Destination directory path.
        - files: List of uploaded files.

        Returns:
        - FilesUploadDto: FilesUploadDto object.
        """
        ...

    @abstractmethod
    def download_schema_to_dto(
        self,
        schema: Any
    ) -> FilesDownloadDto:
        """
        Converts schema object to FilesDownloadDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FilesDownloadDto: FilesDownloadDto object.
        """
        ...

    @abstractmethod
    def move_schema_to_dto(
        self,
        schema: Any
    ) -> FilesMoveDto:
        """
        Converts schema object to FilesMoveDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FilesMoveDto: FilesMoveDto object.
        """
        ...

    @abstractmethod
    def rename_schema_to_dto(
        self,
        schema: Any
    ) -> FileRenameDto:
        """
        Converts schema object to FileRenameDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FileRenameDto: FileRenameDto object.
        """
        ...

    @abstractmethod
    def duplicate_schema_to_dto(
        self,
        schema: Any
    ) -> FilesDuplicateDto:
        """
        Converts schema object to FilesDuplicateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FilesDuplicateDto: FilesDuplicateDto object.
        """
        ...

    @abstractmethod
    def extract_schema_to_dto(
        self,
        schema: Any
    ) -> FilesExtractDto:
        """
        Converts schema object to FilesExtractDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FilesExtractDto: FilesExtractDto object.
        """
        ...

    @abstractmethod
    def delete_schema_to_dto(
        self,
        schema: Any
    ) -> FilesDeleteDto:
        """
        Converts schema object to FilesDeleteDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - FilesDeleteDto: FilesDeleteDto object.
        """
        ...
