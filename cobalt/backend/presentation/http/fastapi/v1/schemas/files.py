#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel, Field, ConfigDict, RootModel


class FileSchema(BaseModel):
    name: str = Field(
        ...,
        title="File name",
        description="File name"
    )

    path: str = Field(
        ...,
        title="Path",
        description="Full path to the file"
    )

    type: Literal["file", "directory"] = Field(
        ...,
        title="Type",
        description="File type"
    )

    format: Optional[str] = Field(
        None,
        title="Format",
        description="File format/extension (e.g. json, txt, jar)"
    )

    size: Optional[int] = Field(
        None,
        title="Size",
        description="File size in bytes, None for directories"
    )

    modified_at: datetime = Field(
        ...,
        title="Modified at",
        description="Last modification timestamp"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "server.properties",
                "path": "/server.properties",
                "type": "file",
                "format": "properties",
                "size": 1024,
                "modified_at": "2024-01-01T12:00:00"
            }
        }
    )

class FilesListSchema(BaseModel):
    files: List[FileSchema] = Field(
        ...,
        title="Files",
        description="List of files and directories"
    )

    path: str = Field(
        ...,
        title="Path",
        description="Current directory path"
    )

    total_files: int = Field(
        ...,
        title="Total files",
        description="Total number of files"
    )

    total_directories: int = Field(
        ...,
        title="Total directories",
        description="Total number of directories"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "files": [
                    {
                        "name": "world",
                        "path": "/world",
                        "type": "directory",
                        "format": None,
                        "size": None,
                        "modified_at": "2024-01-01T12:00:00"
                    },
                    {
                        "name": "server.properties",
                        "path": "/server.properties",
                        "type": "file",
                        "format": "properties",
                        "size": 1024,
                        "modified_at": "2024-01-01T12:00:00"
                    }
                ],
                "path": "/",
                "total_files": 5,
                "total_directories": 5
            }
        }
    )

class FileContentSchema(BaseModel):
    path: str = Field(
        ...,
        title="Path",
        description="Full path to the file"
    )

    name: str = Field(
        ...,
        title="File name",
        description="File name"
    )

    format: Optional[str] = Field(
        None,
        title="Format",
        description="File format/extension"
    )

    size: int = Field(
        ...,
        title="Size",
        description="File size in bytes"
    )

    content: str = Field(
        ...,
        title="Content",
        description="File content (max 3MB)"
    )

    modified_at: datetime = Field(
        ...,
        title="Modified at",
        description="Last modification timestamp"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "path": "/server.properties",
                "name": "server.properties",
                "format": "properties",
                "size": 1024,
                "content": "server-port=25565\nmax-players=20",
                "modified_at": "2024-01-01T12:00:00"
            }
        }
    )

class FilesGetListSchema(BaseModel):
    path: str = Field(
        "/",
        title="Path",
        description="Directory path to list"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "path": "/world"
            }
        }
    )

class FileGetContentSchema(BaseModel):
    path: str = Field(
        ...,
        title="Path",
        description="Path to the file to read"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "path": "/server.properties"
            }
        }
    )

class FilesMoveSchema(BaseModel):
    paths: List[str] = Field(
        ...,
        min_length=1,
        title="Paths",
        description="List of source paths to move"
    )

    destination_path: str = Field(
        ...,
        title="Destination path",
        description="Destination directory path"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "paths": ["/eula.txt", "/ops.json"],
                "destination_path": "/backup"
            }
        }
    )

class FileRenameSchema(BaseModel):
    path: str = Field(
        ...,
        title="Path",
        description="Path to the file or directory to rename"
    )

    name: str = Field(
        ...,
        title="New name",
        description="New name"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "path": "/server.properties",
                "name": "server_old.properties"
            }
        }
    )

class FileSaveContentSchema(BaseModel):
    path: str = Field(
        ...,
        title="Path",
        description="Path to the file to save"
    )

    content: str = Field(
        ...,
        title="Content",
        description="New file content"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "path": "/server.properties",
                "content": "server-port=25565\nmax-players=20"
            }
        }
    )

class FilesDeleteSchema(RootModel):
    root: List[str] = Field(
        ...,
        min_length=1,
        title="Paths",
        description="List of paths to delete"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": ["/banned-ips.json", "/banned-players.json"]
        }
    )

class FilesDownloadSchema(RootModel):
    root: List[str] = Field(
        ...,
        min_length=1,
        title="Paths",
        description="List of paths to download"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": ["/server.properties", "/world"]
        }
    )

class FilesDuplicateSchema(RootModel):
    root: List[str] = Field(
        ...,
        min_length=1,
        title="Paths",
        description="List of paths to duplicate"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": ["/server.properties", "/world"]
        }
    )

class FileCreateSchema(BaseModel):
    path: str = Field(
        ...,
        title="Path",
        description="Path for the new file/directory including name"
    )

    type: Literal["file", "directory"] = Field(
        ...,
        title="Type",
        description="Type of entry to create"
    )

    content: Optional[str] = Field(
        None,
        title="Content",
        description="Initial file content (only for files)"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "path": "/plugins/config.yml",
                "type": "file",
                "content": None
            }
        }
    )

class FilesExtractSchema(BaseModel):
    path: str = Field(
        ...,
        title="Path",
        description="Path to the ZIP archive"
    )

    destination_path: Optional[str] = Field(
        None,
        title="Destination path",
        description="Destination directory path, defaults to archive's parent directory"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "path": "/plugins/myplugin.zip",
                "destination_path": "/plugins"
            }
        }
    )