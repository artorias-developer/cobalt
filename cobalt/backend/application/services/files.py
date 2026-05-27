#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import path
from datetime import datetime, timezone
from pathlib import Path
from typing import List, AsyncIterable, Optional

from aioshutil import copytree, rmtree, move, copy2
from aiofiles import os, open

from domain.exceptions import (
    NotFoundError,
    ConflictError,
    PermissionsError
)
from application.contracts.managers import AbstractArchivesManager
from application.contracts.services import AbstractFilesService
from application.clients.containers.shared import ContainersConstants
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


class FilesService(AbstractFilesService):
    """
    Server filesystem service.
    """
    _MAX_FILE_READ_SIZE = 1 * 1024 * 1024

    app_containers_dir: Path
    archives_manager: AbstractArchivesManager

    def __init__(
        self,
        app_containers_dir: Path,
        archives_manager: AbstractArchivesManager
    ):
        self.app_containers_dir = app_containers_dir
        self.archives_manager = archives_manager

    def _get_server_root(
        self,
        server_id: int
    ) -> Path:
        """
        Returns the absolute root path for the given server container.

        Parameters:
        - server_id: Server ID.

        Returns:
        - Path: Absolute root path.
        """
        container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
            server_id=server_id
        )

        return self.app_containers_dir / container_name

    def _resolve_path(
        self,
        server_id: int,
        relative_path: str
    ) -> Path:
        """
        Resolves and validates that the given relative path stays within the server root.

        Parameters:
        - server_id: Server ID.
        - relative_path: Relative path from the server root.

        Returns:
        - Path: Resolved absolute path.

        Raises:
        - PermissionsError: If the path escapes the server root.
        """
        root = self._get_server_root(server_id)
        resolved = (root / relative_path.lstrip("/")).resolve()

        if not str(resolved).startswith(str(root.resolve())):
            raise PermissionsError("Access outside the server root is not allowed")

        return resolved

    @staticmethod
    def _get_format(
        path: Path
    ) -> Optional[str]:
        """
        Returns the file extension without the leading dot, or None for directories.

        Parameters:
        - path: Path object.

        Returns:
        - str: File extension.
        """
        suffix = path.suffix

        if not suffix:
            return None

        return suffix.lstrip(".")

    async def _collect_paths(
        self,
        server_id: int,
        relative_paths: List[str]
    ) -> List[Path]:
        """
        Resolves and validates that all given relative paths exist.

        Parameters:
        - server_id: Server ID.
        - relative_paths: List of relative paths to resolve.

        Returns:
        - List: List of resolved absolute paths.

        Raises:
        - NotFoundError: If any path does not exist.
        """
        paths = []

        for relative_path in relative_paths:
            target = self._resolve_path(server_id, relative_path)

            if not await os.path.exists(target):
                raise NotFoundError(f'Path "{relative_path}" not found')

            paths.append(target)

        return paths

    async def get_list(
        self,
        server_id: int,
        dto: FilesGetListDto
    ) -> FilesListDto:
        """
        Gets a list of files in the given directory.

        Parameters:
        - server_id: Server ID.
        - dto: FilesListDto object.

        Returns:
        - FilesListDto: FilesListDto object.
        """
        root = self._get_server_root(server_id)
        target = self._resolve_path(server_id, dto.path)

        if not await os.path.exists(target):
            raise NotFoundError(f'Path "{dto.path}" not found')

        if not await os.path.isdir(target):
            raise NotFoundError(f'Path "{dto.path}" is not a directory')

        raw_entries = await os.scandir(target)

        entries = []

        for entry in raw_entries:
            entry_path = Path(entry.path)
            is_dir = await os.path.isdir(entry_path)
            entries.append((entry, entry_path, is_dir))

        entries.sort(key=lambda t: (not t[2], t[0].name.lower()))

        files = []
        total_files = 0
        total_directories = 0

        for entry, entry_path, is_dir in entries:
            stat = await os.stat(entry_path)
            relative = "/" + str(entry_path.relative_to(root))

            files.append(FileDto(
                name=entry_path.name,
                path=relative,
                type="directory" if is_dir else "file",
                format=None if is_dir else self._get_format(entry_path),
                size=None if is_dir else stat.st_size,
                modified_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
            ))

            if is_dir:
                total_directories += 1
            else:
                total_files += 1

        return FilesListDto(
            files=files,
            path=dto.path,
            total_files=total_files,
            total_directories=total_directories
        )

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
        root = self._get_server_root(server_id)
        target = self._resolve_path(server_id, dto.path)

        if not await os.path.exists(target):
            raise NotFoundError(f'File "{dto.path}" not found')

        if not await os.path.isfile(target):
            raise NotFoundError(f'Path "{dto.path}" is not a file')

        stat = await os.stat(target)

        if stat.st_size > self._MAX_FILE_READ_SIZE:
            raise ConflictError(f'File "{dto.path}" exceeds the read limit')

        async with open(target, mode="r", encoding="utf-8", errors="replace") as file:
            content = await file.read()

        return FileContentDto(
            path="/" + str(target.relative_to(root)),
            name=target.name,
            format=self._get_format(target),
            size=stat.st_size,
            content=content,
            modified_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
        )

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
        target = self._resolve_path(server_id, dto.path)

        if not await os.path.exists(target):
            raise NotFoundError(f'File "{dto.path}" not found')

        if not await os.path.isfile(target):
            raise NotFoundError(f'Path "{dto.path}" is not a file')

        async with open(target, mode="w", encoding="utf-8") as file:
            await file.write(dto.content)

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
        target = self._resolve_path(server_id, dto.path)

        if await os.path.exists(target):
            raise ConflictError(f'Path "{dto.path}" already exists')

        if dto.type == "directory":
            await os.makedirs(target, exist_ok=True)
        else:
            parent = path.dirname(target)

            await os.makedirs(parent, exist_ok=True)

            async with open(target, mode="w", encoding="utf-8") as file:
                await file.write(dto.content or "")

    async def upload(
        self,
        server_id: int,
        dto: FilesUploadDto
    ) -> None:
        """
        Uploads a new file.

        Parameters:
        - server_id: Server ID.
        - dto: FileCreateDto object.

        Returns:
        - None.
        """
        destination = self._resolve_path(server_id, dto.path)

        if not await os.path.exists(destination):
            raise NotFoundError(f'Path "{dto.path}" not found')

        if not await os.path.isdir(destination):
            raise NotFoundError(f'Path "{dto.path}" is not a directory')

        for filename, data in dto.files:
            target = destination / filename

            async with open(target, mode="wb") as file:
                await file.write(data)

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
        - AsyncGenerator: Zip archive byte chunks.
        """
        paths = await self._collect_paths(
            server_id=server_id,
            relative_paths=dto.paths
        )

        return await self.archives_manager.stream_zip(
            paths=paths
        )

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
        destination = self._resolve_path(server_id, dto.destination_path)

        if not await os.path.exists(destination):
            raise NotFoundError(f'Destination path "{dto.destination_path}" not found')

        if not await os.path.isdir(destination):
            raise NotFoundError(f'Destination path "{dto.destination_path}" is not a directory')

        sources = await self._collect_paths(
            server_id=server_id,
            relative_paths=dto.paths
        )

        for source in sources:
            await move(str(source), str(destination / source.name))

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
        target = self._resolve_path(server_id, dto.path)

        if not await os.path.exists(target):
            raise NotFoundError(f'Path "{dto.path}" not found')

        destination = target.parent / dto.name

        if await os.path.exists(destination):
            raise ConflictError(f'Name "{dto.name}" is already in use')

        await os.rename(target, destination)

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
        sources = await self._collect_paths(
            server_id=server_id,
            relative_paths=dto.paths
        )

        for source in sources:
            copy_path = source.parent / f"{source.stem}_copy{source.suffix}"
            counter = 1

            while await os.path.exists(copy_path):
                copy_path = source.parent / f"{source.stem}_copy_{counter}{source.suffix}"
                counter += 1

            if await os.path.isdir(source):
                await copytree(str(source), str(copy_path))
            else:
                await copy2(str(source), str(copy_path))

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
        target = self._resolve_path(server_id, dto.path)

        if not await os.path.exists(target):
            raise NotFoundError(f'File "{dto.path}" not found')

        if not await os.path.isfile(target):
            raise NotFoundError(f'Path "{dto.path}" is not a file')

        destination = (
            self._resolve_path(server_id, dto.destination_path)
            if dto.destination_path
            else target.parent
        )

        if dto.destination_path and not await os.path.exists(destination):
            raise NotFoundError(f'Destination path "{dto.destination_path}" not found')

        await self.archives_manager.extract_zip(
            source=target,
            destination=destination
        )

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
        targets = await self._collect_paths(
            server_id=server_id,
            relative_paths=dto.paths
        )

        for target in targets:
            if await os.path.isdir(target):
                await rmtree(str(target))
            else:
                await os.remove(target)
