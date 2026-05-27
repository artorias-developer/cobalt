#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timezone
from pathlib import Path
from stat import S_IFREG
from typing import AsyncGenerator, AsyncIterable, List, Optional, Tuple

from aiofiles import os, open
from stream_unzip import UnzipError, async_stream_unzip
from stream_zip import async_stream_zip, AsyncMemberFile, NO_COMPRESSION_64, Method

from domain.exceptions import ConflictError
from application.contracts.managers import AbstractArchivesManager


class ArchivesManager(AbstractArchivesManager):
    """
    Archives manager.
    """
    _STREAMING_CHUNK_SIZE = 128 * 1024

    @staticmethod
    async def _read_file_chunks(
        path: Path,
        chunk_size: int
    ) -> AsyncGenerator[bytes, None]:
        """
        Reads a file in chunks asynchronously.

        Parameters:
        - path: Absolute path to the file.
        - chunk_size: File read chunk size in bytes.

        Yields:
        - bytes: File content chunk.
        """
        async with open(path, mode="rb") as file:
            while True:
                chunk = await file.read(chunk_size)

                if not chunk:
                    break

                yield chunk

    async def _walk_dir(
        self,
        base: Path,
        current: Path,
        chunk_size: int,
        compression: Method
    ) -> AsyncGenerator[AsyncMemberFile, None]:
        """
        Recursively walks a directory and yields async_stream_zip member tuples.

        Parameters:
        - base: Absolute path to the root directory being archived (used for arc name).
        - current: Absolute path to the directory currently being walked.
        - chunk_size: File read chunk size in bytes.
        - compression: stream_zip compression method.

        Yields:
        - AsyncMemberFile: Member tuple for async_stream_zip.
        """
        entries = await os.scandir(current)

        directories = []
        files = []

        for entry in entries:
            entry_path = Path(entry.path)

            if await os.path.isdir(entry_path):
                directories.append(entry_path)
            else:
                files.append(entry_path)

        for file_path in sorted(files, key=lambda p: p.name):
            stat = await os.stat(file_path)
            modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
            arc_name = str(Path(base.name) / file_path.relative_to(base))

            yield (
                arc_name,
                modified_at,
                S_IFREG | 0o600,
                compression,
                self._read_file_chunks(file_path, chunk_size)
            )

        for directory in sorted(directories, key=lambda p: p.name):
            async for member in self._walk_dir(base, directory, chunk_size, compression):
                yield member

    async def _collect_members(
        self,
        paths: List[Path],
        chunk_size: int,
        compression: Method
    ) -> AsyncGenerator[AsyncMemberFile, None]:
        """
        Yields async_stream_zip member tuples for all given paths recursively.

        Parameters:
        - paths: List of resolved absolute paths.
        - chunk_size: File read chunk size in bytes.
        - compression: stream_zip compression method.

        Yields:
        - AsyncMemberFile: Member tuple for async_stream_zip.
        """
        for target in paths:
            if await os.path.isdir(target):
                async for member in self._walk_dir(target, target, chunk_size, compression):
                    yield member
            else:
                stat = await os.stat(target)
                modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)

                yield (
                    target.name,
                    modified_at,
                    S_IFREG | 0o600,
                    compression,
                    self._read_file_chunks(target, chunk_size)
                )

    def _resolve_params(
        self,
        chunk_size: Optional[int] = None,
        compression: Optional[Method] = None
    ) -> Tuple[int, Method]:
        """
        Resolves chunk size and compression to their defaults if not provided.

        Parameters:
        - chunk_size: File read chunk size in bytes, or None to use default.
        - compression: stream_zip compression method, or None to use default.

        Returns:
        - Tuple: Resolved chunk size and compression method.
        """
        return (
            chunk_size if chunk_size is not None else self._STREAMING_CHUNK_SIZE,
            compression if compression is not None else NO_COMPRESSION_64
        )

    async def create_zip(
        self,
        paths: List[Path],
        destination: Path,
        chunk_size: Optional[int] = None,
        compression: Optional[Method] = None
    ) -> Path:
        """
        Creates a ZIP archive from the given paths and writes it to destination.

        Parameters:
        - paths: List of resolved absolute paths to archive.
        - destination: Path where the ZIP file will be written.
        - chunk_size: File read chunk size in bytes. Defaults to 128 KiB.
        - compression: Compression method. Defaults to NO_COMPRESSION_64.

        Returns:
        - Path: Path to the written ZIP file.
        """
        chunk_size, compression = self._resolve_params(chunk_size, compression)

        async with open(destination, mode="wb") as dest_file:
            async for chunk in async_stream_zip(
                files=self._collect_members(paths, chunk_size, compression)
            ):
                await dest_file.write(chunk)

        return destination

    async def stream_zip(
        self,
        paths: List[Path],
        chunk_size: Optional[int] = None,
        compression: Optional[Method] = None
    ) -> AsyncIterable[bytes]:
        """
        Creates a ZIP archive from the given paths and streams it as byte chunks.

        Parameters:
        - paths: List of resolved absolute paths to archive.
        - chunk_size: File read chunk size in bytes. Defaults to 128 KiB.
        - compression: Compression method. Defaults to NO_COMPRESSION_64.

        Returns:
        - AsyncIterable: ZIP archive byte chunks.
        """
        chunk_size, compression = self._resolve_params(chunk_size, compression)

        return async_stream_zip(
            files=self._collect_members(paths, chunk_size, compression)
        )

    async def extract_zip(
        self,
        source: Path,
        destination: Path
    ) -> None:
        """
        Extracts a ZIP archive to the destination path.

        Parameters:
        - source: Absolute path to the ZIP archive.
        - destination: Absolute path to the destination directory.

        Returns:
        - None.
        """
        try:
            async for file_name, _, unzipped_chunks in async_stream_unzip(
                self._read_file_chunks(source, self._STREAMING_CHUNK_SIZE)
            ):
                decoded = file_name.decode()
                file_path = destination / decoded

                if decoded.endswith("/"):
                    if await os.path.isfile(file_path):
                        raise ConflictError(f'Path "{decoded.rstrip("/")}" already exists')

                    await os.makedirs(file_path, exist_ok=True)

                    async for _ in unzipped_chunks:
                        pass
                    continue

                await os.makedirs(file_path.parent, exist_ok=True)

                async with open(file_path, mode="wb") as f:
                    async for chunk in unzipped_chunks:
                        await f.write(chunk)
        except UnzipError:
            raise ConflictError(f'File "{source.name}" is not a valid ZIP archive')