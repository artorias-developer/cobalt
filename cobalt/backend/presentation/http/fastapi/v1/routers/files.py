#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from fastapi import APIRouter, Response, status, Depends, Body, Query, File, UploadFile
from fastapi.responses import StreamingResponse

from domain.enums import PermissionsEnum
from application.contracts.services import (
    AbstractFilesService,
    AbstractAuthService
)
from presentation.contracts.http.routers import AbstractHttpFilesRouter
from presentation.contracts.http.mappers import AbstractFilesRouterMapper
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import (
    FilesGetListSchema,
    FilesListSchema,
    FileGetContentSchema,
    FileContentSchema,
    FilesMoveSchema,
    FileRenameSchema,
    FileSaveContentSchema,
    FilesDuplicateSchema,
    FilesDeleteSchema,
    FilesDownloadSchema,
    FileCreateSchema,
    FilesExtractSchema
)


class HttpFilesRouter(AbstractHttpFilesRouter, HttpBaseRouter):
    """
    Handles HTTP routes for server files operations.
    """
    router: APIRouter
    files_service: AbstractFilesService
    files_mapper: AbstractFilesRouterMapper

    def __init__(
        self,
        router: APIRouter,
        files_service: AbstractFilesService,
        files_mapper: AbstractFilesRouterMapper,
        auth_service: AbstractAuthService
    ):
        HttpBaseRouter.__init__(self, auth_service)

        self.router = router
        self.files_service = files_service
        self.files_mapper = files_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/servers/{server_id}/files",
            tags=["Files"],
            dependencies=[
                Depends(self.http_session_required)
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.get_list,
            methods=["GET"],
            operation_id="files_get_list",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/content",
            endpoint=self.get_content,
            methods=["GET"],
            operation_id="files_get_content",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/content",
            endpoint=self.save_content,
            methods=["PUT"],
            operation_id="files_save_content",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.create,
            methods=["POST"],
            operation_id="files_create",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/upload",
            endpoint=self.upload,
            methods=["POST"],
            operation_id="files_upload",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/download",
            endpoint=self.download,
            methods=["POST"],
            operation_id="files_download",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_DOWNLOAD
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/move",
            endpoint=self.move,
            methods=["POST"],
            operation_id="files_move",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/rename",
            endpoint=self.rename,
            methods=["POST"],
            operation_id="files_rename",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/duplicate",
            endpoint=self.duplicate,
            methods=["POST"],
            operation_id="files_duplicate",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/extract",
            endpoint=self.extract,
            methods=["POST"],
            operation_id="files_extract",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_UPDATE
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/",
            endpoint=self.delete,
            methods=["DELETE"],
            operation_id="files_delete",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_FILES_UPDATE
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def get_list(
        self,
        server_id: int,
        schema: FilesGetListSchema = Depends()
    ) -> FilesListSchema:
        """
        Gets a list of entries in the given directory.

        Parameters:
        - server_id: Server ID.
        - schema: FilesGetListSchema object.

        Returns:
        - FilesListSchema: FilesListSchema object.
        """
        request_dto = self.files_mapper.get_list_schema_to_dto(
            schema=schema
        )

        response_dto = await self.files_service.get_list(
            server_id=server_id,
            dto=request_dto
        )

        return self.files_mapper.list_dto_to_schema(
            dto=response_dto
        )

    async def get_content(
        self,
        server_id: int,
        schema: FileGetContentSchema = Depends()
    ) -> FileContentSchema:
        """
        Gets the content of a specific file.

        Parameters:
        - server_id: Server ID.
        - schema: FileGetContentSchema object.

        Returns:
        - FileContentSchema: FileContentSchema object.
        """
        request_dto = self.files_mapper.get_content_schema_to_dto(
            schema=schema
        )

        response_dto = await self.files_service.get_content(
            server_id=server_id,
            dto=request_dto
        )

        return self.files_mapper.content_dto_to_schema(
            dto=response_dto
        )

    async def save_content(
        self,
        server_id: int,
        schema: FileSaveContentSchema = Body(...)
    ) -> Response:
        """
        Saves the content of a specific file.

        Parameters:
        - server_id: Server ID.
        - schema: FileSaveContentSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.files_mapper.save_content_schema_to_dto(
            schema=schema
        )

        await self.files_service.save_content(
            server_id=server_id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def create(
        self,
        server_id: int,
        schema: FileCreateSchema = Body(...)
    ) -> Response:
        """
        Creates a new file.

        Parameters:
        - server_id: Server ID.
        - schema: FileCreateSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.files_mapper.create_schema_to_dto(
            schema=schema
        )

        await self.files_service.create(
            server_id=server_id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def upload(
        self,
        server_id: int,
        path: str = Query(...),
        files: List[UploadFile] = File(...)
    ) -> Response:
        """
        Uploads one or multiple files to the given directory.

        Parameters:
        - server_id: Server ID.
        - path: Destination directory path.
        - files: Uploaded files.

        Returns:
        - Response: Response object.
        """
        request_dto = await self.files_mapper.upload_schema_to_dto(
            path=path,
            files=files
        )

        await self.files_service.upload(
            server_id=server_id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def download(
        self,
        server_id: int,
        schema: FilesDownloadSchema = Body(...)
    ) -> StreamingResponse:
        """
        Downloads one or multiple files/directories as a zip archive.

        Parameters:
        - server_id: Server ID.
        - schema: FilesDownloadSchema object.

        Returns:
        - StreamingResponse: Zip archive stream.
        """
        request_dto = self.files_mapper.download_schema_to_dto(
            schema=schema
        )

        stream = await self.files_service.download(
            server_id=server_id,
            dto=request_dto
        )

        return StreamingResponse(
            content=stream,
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=cobalt_server_{server_id}_files.zip"
            }
        )

    async def move(
        self,
        server_id: int,
        schema: FilesMoveSchema = Body(...)
    ) -> Response:
        """
        Moves one or multiple files/directories to the destination path.

        Parameters:
        - server_id: Server ID.
        - schema: FilesMoveSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.files_mapper.move_schema_to_dto(
            schema=schema
        )

        await self.files_service.move(
            server_id=server_id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def rename(
        self,
        server_id: int,
        schema: FileRenameSchema = Body(...)
    ) -> Response:
        """
        Renames a file or directory.

        Parameters:
        - server_id: Server ID.
        - schema: FileRenameSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.files_mapper.rename_schema_to_dto(
            schema=schema
        )

        await self.files_service.rename(
            server_id=server_id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def duplicate(
        self,
        server_id: int,
        schema: FilesDuplicateSchema = Body(...)
    ) -> Response:
        """
        Duplicates one or multiple files/directories.

        Parameters:
        - server_id: Server ID.
        - schema: FilesDuplicateSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.files_mapper.duplicate_schema_to_dto(
            schema=schema
        )

        await self.files_service.duplicate(
            server_id=server_id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def extract(
        self,
        server_id: int,
        schema: FilesExtractSchema = Body(...)
    ) -> Response:
        """
        Extracts a ZIP archive to the destination path.

        Parameters:
        - server_id: Server ID.
        - schema: FilesExtractSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.files_mapper.extract_schema_to_dto(
            schema=schema
        )

        await self.files_service.extract(
            server_id=server_id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def delete(
        self,
        server_id: int,
        schema: FilesDeleteSchema = Body(...)
    ) -> Response:
        """
        Deletes one or multiple files/directories.

        Parameters:
        - server_id: Server ID.
        - schema: FilesDeleteSchema object.

        Returns:
        - Response: Response object.
        """
        request_dto = self.files_mapper.delete_schema_to_dto(
            schema=schema
        )

        await self.files_service.delete(
            server_id=server_id,
            dto=request_dto
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )