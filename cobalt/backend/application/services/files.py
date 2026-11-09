#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timezone
from pathlib import Path
from stat import S_ISDIR, S_ISREG
from typing import List, AsyncIterable, Optional

from aioshutil import copytree, rmtree, move, copy2
from aiofiles import os, open

from domain.enums import FileTypeEnum
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
        Returns the resolved absolute root path for the given server container.

        Parameters:
        - server_id: Server ID.

        Returns:
        - Path: Resolved absolute root path.
        """
        container_name = ContainersConstants.SERVER_RUNTIME_KEY.format(
            server_id=server_id
        )

        return (self.app_containers_dir / container_name).resolve()

    def _resolve_path(
        self,
        server_id: int,
        relative_path: str,
        allow_root: bool = True
    ) -> Path:
        """
        Resolves and validates that the given relative path stays within the server root.

        Parameters:
        - server_id: Server ID.
        - relative_path: Relative path from the server root.
        - allow_root: Whether the server root itself is an acceptable result.

        Returns:
        - Path: Resolved absolute path.

        Raises:
        - PermissionsError: If the path escapes the server root (or is the root when not allowed).
        """
        root = self._get_server_root(server_id)
        resolved = (root / relative_path.lstrip("/")).resolve()

        if not resolved.is_relative_to(root):
            raise PermissionsError("Access outside the server root is not allowed")

        if not allow_root and resolved == root:
            raise PermissionsError("Operation on the server root is not allowed")

        return resolved

    @staticmethod
    def _validate_name(
        name: str
    ) -> None:
        """
        Validates that the given value is a plain file or directory name
        (no separators, no traversal components).

        Parameters:
        - name: File or directory name.

        Raises:
        - PermissionsError: If the name is not a plain name.
        """
        if (
            not name
            or name in (".", "..")
            or "/" in name
            or "\\" in name
            or "\0" in name
            or Path(name).name != name
        ):
            raise PermissionsError("Invalid file name")

    @staticmethod
    def _get_format(
        file_path: Path
    ) -> Optional[str]:
        """
        Returns the file extension without the leading dot, or None for directories.

        Parameters:
        - path: Path object.

        Returns:
        - str: File extension.
        """
        suffix = file_path.suffix

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
        The server root itself is not accepted.

        Parameters:
        - server_id: Server ID.
        - relative_paths: List of relative paths to resolve.

        Returns:
        - List: List of resolved absolute paths.

        Raises:
        - NotFoundError: If any path does not exist.
        - PermissionsError: If any path is outside the root or is the root itself.
        """
        paths = []

        for relative_path in relative_paths:
            target = self._resolve_path(server_id, relative_path, allow_root=False)

            if not await os.path.exists(target):
                raise NotFoundError('Path "{relative_path}" not found', relative_path=relative_path)

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

        try:
            raw_entries = await os.scandir(target)
        except FileNotFoundError:
            raise NotFoundError('Path "{path}" not found', path=dto.path)
        except NotADirectoryError:
            raise NotFoundError('Path "{path}" is not a directory', path=dto.path)

        entries = []

        for entry in raw_entries:
            entry_path = Path(entry.path)

            try:
                stat = await os.stat(entry_path)
            except FileNotFoundError:
                continue

            entries.append((entry_path, stat, S_ISDIR(stat.st_mode)))

        entries.sort(key=lambda t: (not t[2], t[0].name.lower()))

        files = []
        total_files = 0
        total_directories = 0

        for entry_path, stat, is_dir in entries:
            relative = "/" + str(entry_path.relative_to(root))

            files.append(FileDto(
                name=entry_path.name,
                path=relative,
                type=FileTypeEnum.DIRECTORY if is_dir else FileTypeEnum.FILE,
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

        try:
            stat = await os.stat(target)
        except FileNotFoundError:
            raise NotFoundError('File "{path}" not found', path=dto.path)

        if not S_ISREG(stat.st_mode):
            raise NotFoundError('Path "{path}" is not a file', path=dto.path)

        if stat.st_size > self._MAX_FILE_READ_SIZE:
            raise ConflictError('File "{path}" exceeds the read limit', path=dto.path)

        try:
            async with open(target, mode="r", encoding="utf-8", errors="replace") as file:
                content = await file.read()
        except FileNotFoundError:
            raise NotFoundError('File "{path}" not found', path=dto.path)
        except IsADirectoryError:
            raise NotFoundError('Path "{path}" is not a file', path=dto.path)

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
        Saves the content of an existing file. Does not create the file if it is missing.

        Parameters:
        - server_id: Server ID.
        - dto: FileSaveContentDto object.

        Returns:
        - None.
        """
        target = self._resolve_path(server_id, dto.path)

        try:
            async with open(target, mode="r+", encoding="utf-8") as file:
                await file.seek(0)
                await file.write(dto.content)
                await file.truncate()
        except FileNotFoundError:
            raise NotFoundError('File "{path}" not found', path=dto.path)
        except IsADirectoryError:
            raise NotFoundError('Path "{path}" is not a file', path=dto.path)

    async def create(
        self,
        server_id: int,
        dto: FileCreateDto
    ) -> None:
        """
        Creates a new file or directory.

        Parameters:
        - server_id: Server ID.
        - dto: FileCreateDto object.

        Returns:
        - None.
        """
        target = self._resolve_path(server_id, dto.path, allow_root=False)

        try:
            if dto.type == "directory":
                await os.makedirs(target, exist_ok=False)
            else:
                await os.makedirs(target.parent, exist_ok=True)

                async with open(target, mode="x", encoding="utf-8") as file:
                    await file.write(dto.content or "")
        except (FileExistsError, NotADirectoryError):
            raise ConflictError('Path "{path}" already exists', path=dto.path)

    async def upload(
        self,
        server_id: int,
        dto: FilesUploadDto
    ) -> None:
        """
        Uploads new files. Existing files with the same name are overwritten.

        Parameters:
        - server_id: Server ID.
        - dto: FileCreateDto object.

        Returns:
        - None.
        """
        destination = self._resolve_path(server_id, dto.path)

        if not await os.path.isdir(destination):
            raise NotFoundError('Path "{path}" is not a directory', path=dto.path)

        for filename, _ in dto.files:
            self._validate_name(filename)

        for filename, data in dto.files:
            target = destination / filename

            try:
                async with open(target, mode="wb") as file:
                    await file.write(data)
            except FileNotFoundError:
                raise NotFoundError('Path "{path}" not found', path=dto.path)
            except IsADirectoryError:
                raise ConflictError('Path "{name}" is a directory', name=filename)

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
            raise NotFoundError('Destination path "{path}" not found', path=dto.destination_path)

        if not await os.path.isdir(destination):
            raise NotFoundError('Destination path "{path}" is not a directory', path=dto.destination_path)

        sources = await self._collect_paths(
            server_id=server_id,
            relative_paths=dto.paths
        )

        for source in sources:
            new_path = destination / source.name

            if await os.path.exists(new_path):
                raise ConflictError('Name "{name}" is already in use', name=source.name)

            try:
                await move(str(source), str(new_path))
            except FileNotFoundError:
                raise NotFoundError('Path "{path}" not found', path=source.name)

    async def rename(
        self,
        server_id: int,
        dto: FileRenameDto
    ) -> None:
        """
        Renames a file or directory.

        Parameters:
        - server_id: Server ID.
        - dto: FileRenameDto object (dto.overwrite: replace an existing file with the new name,
          disabled by default; directories are never overwritten).

        Returns:
        - None.
        """
        self._validate_name(dto.name)

        target = self._resolve_path(server_id, dto.path, allow_root=False)
        destination = target.parent / dto.name

        if not await os.path.exists(target):
            raise NotFoundError('Path "{path}" not found', path=dto.path)

        if destination == target:
            return

        try:
            if dto.overwrite:
                if await os.path.isdir(destination):
                    raise ConflictError('Directory "{name}" cannot be overwritten', name=dto.name)

                await os.replace(target, destination)
            else:
                if await os.path.exists(destination):
                    raise ConflictError('Name "{name}" is already in use', name=dto.name)

                await os.rename(target, destination)
        except FileNotFoundError:
            raise NotFoundError('Path "{path}" not found', path=dto.path)
        except (IsADirectoryError, NotADirectoryError):
            raise ConflictError('Name "{name}" is already in use', name=dto.name)

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

            try:
                if await os.path.isdir(source):
                    await copytree(str(source), str(copy_path))
                else:
                    await copy2(str(source), str(copy_path))
            except FileNotFoundError:
                raise NotFoundError('Path "{path}" not found', path=source.name)

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
            raise NotFoundError('File "{path}" not found', path=dto.path)

        if not await os.path.isfile(target):
            raise NotFoundError('Path "{path}" is not a file', path=dto.path)

        destination = (
            self._resolve_path(server_id, dto.destination_path)
            if dto.destination_path
            else target.parent
        )

        if dto.destination_path and not await os.path.isdir(destination):
            raise NotFoundError('Destination path "{path}" is not a directory', path=dto.destination_path)

        try:
            await self.archives_manager.extract_zip(
                source=target,
                destination=destination
            )
        except FileNotFoundError:
            raise NotFoundError('File "{path}" not found', path=dto.path)

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
            try:
                if await os.path.isdir(target):
                    await rmtree(str(target))
                else:
                    await os.remove(target)
            except FileNotFoundError:
                pass