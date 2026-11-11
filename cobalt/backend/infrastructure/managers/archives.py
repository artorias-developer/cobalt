#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timezone
from pathlib import Path
from stat import S_IFREG
from typing import AsyncGenerator, AsyncIterable, List, Optional, Tuple

from aiofiles import os, open
from stream_unzip import UnzipError, async_stream_unzip
from stream_zip import async_stream_zip, AsyncMemberFile, NO_COMPRESSION_64, Method

from domain.exceptions import (
    ConflictError,
    PermissionsError
)
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

    @staticmethod
    def _decode_name(
        raw_name: bytes
    ) -> str:
        """
        Decodes a ZIP entry name. Falls back to CP437 (the ZIP default) for non-UTF-8 names.

        Parameters:
        - raw_name: Raw entry name.

        Returns:
        - str: Decoded entry name.
        """
        try:
            return raw_name.decode("utf-8")
        except UnicodeDecodeError:
            return raw_name.decode("cp437")

    async def _walk_dir(
        self,
        base: Path,
        current: Path,
        chunk_size: int,
        compression: Method
    ) -> AsyncGenerator[AsyncMemberFile, None]:
        """
        Recursively walks a directory and yields async_stream_zip member tuples.
        Symlinks and special files (sockets, FIFOs, devices) are skipped, so the archive
        can never include anything from outside the walked directory and cannot loop.
        Entries that disappear during the walk are skipped.

        Parameters:
        - base: Absolute path to the root directory being archived (used for arc name).
        - current: Absolute path to the directory currently being walked.
        - chunk_size: File read chunk size in bytes.
        - compression: stream_zip compression method.

        Yields:
        - AsyncMemberFile: Member tuple for async_stream_zip.
        """
        try:
            entries = await os.scandir(current)
        except (FileNotFoundError, NotADirectoryError):
            return

        directories = []
        files = []

        for entry in entries:
            entry_path = Path(entry.path)

            try:
                if entry.is_symlink():
                    continue

                if entry.is_dir(follow_symlinks=False):
                    directories.append(entry_path)
                elif entry.is_file(follow_symlinks=False):
                    files.append(entry_path)
            except OSError:
                continue

        for file_path in sorted(files, key=lambda p: p.name):
            try:
                stat = await os.stat(file_path)
            except FileNotFoundError:
                continue

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
                try:
                    stat = await os.stat(target)
                except FileNotFoundError:
                    continue

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
        Every entry is validated to stay inside the destination directory (zip-slip protection),
        including entries that pass through already existing symlinks.

        Parameters:
        - source: Absolute path to the ZIP archive.
        - destination: Absolute path to the destination directory.

        Returns:
        - None.

        Raises:
        - PermissionsError: If an entry points outside the destination directory.
        - ConflictError: If the archive is invalid or an entry conflicts with an existing path.
        """
        root = destination.resolve()

        try:
            async for raw_name, _, unzipped_chunks in async_stream_unzip(
                self._read_file_chunks(source, self._STREAMING_CHUNK_SIZE)
            ):
                decoded = self._decode_name(raw_name)
                is_directory = decoded.endswith("/")
                file_path = (root / decoded).resolve()

                if not file_path.is_relative_to(root):
                    raise PermissionsError('Archive entry "{name}" points outside the destination', name=decoded)

                if file_path == root:
                    if not is_directory:
                        raise PermissionsError('Archive entry "{name}" is not a valid file name', name=decoded)

                    async for _ in unzipped_chunks:
                        pass
                    continue

                try:
                    if is_directory:
                        await os.makedirs(file_path, exist_ok=True)

                        async for _ in unzipped_chunks:
                            pass
                        continue

                    await os.makedirs(file_path.parent, exist_ok=True)

                    async with open(file_path, mode="wb") as f:
                        async for chunk in unzipped_chunks:
                            await f.write(chunk)
                except (FileExistsError, NotADirectoryError, IsADirectoryError):
                    raise ConflictError('Path "{path}" already exists', path=decoded.rstrip("/"))
        except UnzipError:
            raise ConflictError('File "{name}" is not a valid ZIP archive', name=source.name)