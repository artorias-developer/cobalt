#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path
from abc import ABC, abstractmethod
from typing import AsyncIterable, Optional, Any, List


class AbstractArchivesManager(ABC):
    """
    Abstract archives manager.
    """

    @abstractmethod
    async def create_zip(
        self,
        paths: List[Path],
        destination: Path,
        chunk_size: Optional[int] = None,
        compression: Optional[Any] = None
    ) -> Path:
        """
        Creates an archive from the given paths and writes it to destination.

        Parameters:
        - paths: List of resolved absolute paths to archive.
        - destination: Path where the archive file will be written.
        - chunk_size: File read chunk size in bytes.
        - compression: Compression method.

        Returns:
        - Path: Path to the written archive file.
        """
        ...

    @abstractmethod
    async def stream_zip(
        self,
        paths: List[Path],
        chunk_size: Optional[int] = None,
        compression: Optional[Any] = None
    ) -> AsyncIterable[bytes]:
        """
        Creates an archive from the given paths and streams it as byte chunks.

        Parameters:
        - paths: List of resolved absolute paths to archive.
        - chunk_size: File read chunk size in bytes.
        - compression: Compression method.

        Returns:
        - AsyncIterable: Archive byte chunks.
        """
        ...

    @abstractmethod
    async def extract_zip(
        self,
        source: Path,
        destination: Path
    ) -> None:
        """
        Extracts an archive to the destination path.

        Parameters:
        - source: Absolute path to the archive file.
        - destination: Absolute path to the destination directory.

        Returns:
        - None.
        """
        ...