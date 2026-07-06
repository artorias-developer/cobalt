#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List, Literal

from application.dtos.base import BaseDto


class FileDto(BaseDto):
    name: str
    path: str
    type: Literal["file", "directory"]
    format: Optional[str] = None
    size: Optional[int] = None
    modified_at: datetime

class FilesListDto(BaseDto):
    files: List[FileDto]
    path: str
    total_files: int
    total_directories: int

class FileContentDto(BaseDto):
    path: str
    name: str
    format: Optional[str] = None
    size: int
    content: str
    modified_at: datetime

class FilesGetListDto(BaseDto):
    path: Optional[str] = None

class FileGetContentDto(BaseDto):
    path: str

class FilesMoveDto(BaseDto):
    paths: List[str]
    destination_path: str

class FileRenameDto(BaseDto):
    path: str
    name: str

class FilesDuplicateDto(BaseDto):
    paths: List[str]

class FilesDeleteDto(BaseDto):
    paths: List[str]

class FilesDownloadDto(BaseDto):
    paths: List[str]

class FileSaveContentDto(BaseDto):
    path: str
    content: str

class FileCreateDto(BaseDto):
    path: str
    type: Literal["file", "directory"]
    content: Optional[str] = None

class FilesUploadDto(BaseDto):
    path: str
    files: List[tuple[str, bytes]]

class FilesExtractDto(BaseDto):
    path: str
    destination_path: Optional[str] = None