#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from fastapi import UploadFile

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
from presentation.contracts.http.mappers import AbstractFilesRouterMapper
from presentation.http.fastapi.v1.schemas import (
    FileSchema,
    FilesGetListSchema,
    FilesListSchema,
    FileGetContentSchema,
    FileContentSchema,
    FilesMoveSchema,
    FileRenameSchema,
    FilesDuplicateSchema,
    FilesDeleteSchema,
    FilesDownloadSchema,
    FileSaveContentSchema,
    FileCreateSchema,
    FilesExtractSchema
)


class FilesRouterMapper(AbstractFilesRouterMapper):
    """
    Mapper for files router.
    """

    def dto_to_schema(
        self,
        dto: FileDto
    ) -> FileSchema:
        """
        Converts FileDto object to FileSchema object.

        Parameters:
        - dto: FileDto object.

        Returns:
        - FileSchema: FileSchema object.
        """
        return FileSchema(
            name=dto.name,
            path=dto.path,
            type=dto.type,
            format=dto.format,
            size=dto.size,
            modified_at=dto.modified_at
        )

    def list_dto_to_schema(
        self,
        dto: FilesListDto
    ) -> FilesListSchema:
        """
        Converts FilesListDto object to FilesListSchema object.

        Parameters:
        - dto: FilesListDto object.

        Returns:
        - FilesListSchema: FilesListSchema object.
        """
        return FilesListSchema(
            files=[
                self.dto_to_schema(file)
                for file in dto.files
            ],
            path=dto.path,
            total_files=dto.total_files,
            total_directories=dto.total_directories
        )

    def content_dto_to_schema(
        self,
        dto: FileContentDto
    ) -> FileContentSchema:
        """
        Converts FileContentDto object to FileContentSchema object.

        Parameters:
        - dto: FileContentDto object.

        Returns:
        - FileContentSchema: FileContentSchema object.
        """
        return FileContentSchema(
            path=dto.path,
            name=dto.name,
            format=dto.format,
            size=dto.size,
            content=dto.content,
            modified_at=dto.modified_at
        )

    def get_list_schema_to_dto(
        self,
        schema: FilesGetListSchema
    ) -> FilesGetListDto:
        """
        Converts FilesGetListSchema object to FilesGetListDto object.

        Parameters:
        - schema: FilesGetListSchema object.

        Returns:
        - FilesGetListDto: FilesGetListDto object.
        """
        return FilesGetListDto(
            path=schema.path
        )

    def get_content_schema_to_dto(
        self,
        schema: FileGetContentSchema
    ) -> FileGetContentDto:
        """
        Converts FileGetContentSchema object to FileGetContentDto object.

        Parameters:
        - schema: FileGetContentSchema object.

        Returns:
        - FileGetContentDto: FileGetContentDto object.
        """
        return FileGetContentDto(
            path=schema.path
        )

    def save_content_schema_to_dto(
        self,
        schema: FileSaveContentSchema
    ) -> FileSaveContentDto:
        """
        Converts FileSaveContentSchema object to FileSaveContentDto object.

        Parameters:
        - schema: FileSaveContentSchema object.

        Returns:
        - FileSaveContentDto: FileSaveContentDto object.
        """
        return FileSaveContentDto(
            path=schema.path,
            content=schema.content
        )

    def create_schema_to_dto(
        self,
        schema: FileCreateSchema
    ) -> FileCreateDto:
        """
        Converts FileCreateSchema object to FileCreateDto object.

        Parameters:
        - schema: FileCreateSchema object.

        Returns:
        - FileCreateDto: FileCreateDto object.
        """
        return FileCreateDto(
            path=schema.path,
            type=schema.type,
            content=schema.content
        )

    async def upload_schema_to_dto(
        self,
        path: str,
        files: List[UploadFile]
    ) -> FilesUploadDto:
        """
        Converts upload request parameters to FilesUploadDto object.

        Parameters:
        - path: Destination directory path.
        - files: List of uploaded files.

        Returns:
        - FilesUploadDto: FilesUploadDto object.
        """
        return FilesUploadDto(
            path=path,
            files=[
                (file.filename, await file.read())
                for file in files
            ]
        )

    def download_schema_to_dto(
        self,
        schema: FilesDownloadSchema
    ) -> FilesDownloadDto:
        """
        Converts FilesDownloadSchema object to FilesDownloadDto object.

        Parameters:
        - schema: FilesDownloadSchema object.

        Returns:
        - FilesDownloadDto: FilesDownloadDto object.
        """
        return FilesDownloadDto(
            paths=schema.root
        )

    def move_schema_to_dto(
        self,
        schema: FilesMoveSchema
    ) -> FilesMoveDto:
        """
        Converts FilesMoveSchema object to FilesMoveDto object.

        Parameters:
        - schema: FilesMoveSchema object.

        Returns:
        - FilesMoveDto: FilesMoveDto object.
        """
        return FilesMoveDto(
            paths=schema.paths,
            destination_path=schema.destination_path
        )

    def rename_schema_to_dto(
        self,
        schema: FileRenameSchema
    ) -> FileRenameDto:
        """
        Converts FileRenameSchema object to FileRenameDto object.

        Parameters:
        - schema: FileRenameSchema object.

        Returns:
        - FileRenameDto: FileRenameDto object.
        """
        return FileRenameDto(
            path=schema.path,
            name=schema.name
        )

    def duplicate_schema_to_dto(
        self,
        schema: FilesDuplicateSchema
    ) -> FilesDuplicateDto:
        """
        Converts FilesDuplicateSchema object to FilesDuplicateDto object.

        Parameters:
        - schema: FilesDuplicateSchema object.

        Returns:
        - FilesDuplicateDto: FilesDuplicateDto object.
        """
        return FilesDuplicateDto(
            paths=schema.root
        )

    def extract_schema_to_dto(
        self,
        schema: FilesExtractSchema
    ) -> FilesExtractDto:
        """
        Converts FilesExtractSchema object to FilesExtractDto object.

        Parameters:
        - schema: FilesExtractSchema object.

        Returns:
        - FilesExtractDto: FilesExtractDto object.
        """
        return FilesExtractDto(
            path=schema.path,
            destination_path=schema.destination_path
        )

    def delete_schema_to_dto(
        self,
        schema: FilesDeleteSchema
    ) -> FilesDeleteDto:
        """
        Converts FilesDeleteSchema object to FilesDeleteDto object.

        Parameters:
        - schema: FilesDeleteSchema object.

        Returns:
        - FilesDeleteDto: FilesDeleteDto object.
        """
        return FilesDeleteDto(
            paths=schema.root
        )
