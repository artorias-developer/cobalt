#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from fastapi import status

from domain.enums import FileTypeEnum, PermissionEnum
from domain.exceptions import ConflictError, NotFoundError, ValidationError
from application.dtos import (
    FilesListDto,
    FileContentDto,
    FilesGetListDto,
    FileGetContentDto,
    FileSaveContentDto,
    FileCreateDto,
    FilesUploadDto,
    FilesDownloadDto,
    FilesMoveDto,
    FileRenameDto,
    FilesDuplicateDto,
    FilesExtractDto,
    FilesDeleteDto
)
from presentation.http.fastapi.v1.mappers import FilesRouterMapper
from presentation.http.fastapi.v1.routers import HttpFilesRouter

from helpers.app import build_test_client
from helpers.factories import NOW, make_file_dto
from helpers.routes import Route, RouteContract


SERVER_ID = 2
URL = f"/api/v1/servers/{SERVER_ID}/files"
NO_CONTENT = status.HTTP_204_NO_CONTENT

LISTING = FilesListDto(
    files=[
        make_file_dto(name="world", path="/world", file_type=FileTypeEnum.DIRECTORY),
        make_file_dto()
    ],
    path="/",
    total_files=1,
    total_directories=1
)
CONTENT = FileContentDto(
    path="/server.properties",
    name="server.properties",
    format="properties",
    size=12,
    content="motd=Cobalt",
    modified_at=NOW
)


async def _zip_stream():
    yield b"PK\x03\x04"
    yield b"rest-of-archive"


@pytest.fixture
def service(files_service_mock):
    return files_service_mock


@pytest.fixture
def client(files_service_mock, auth_service_mock, i18n_manager, logger):
    with build_test_client(
        router_factories=[
            lambda api: HttpFilesRouter(
                router=api,
                files_service=files_service_mock,
                files_mapper=FilesRouterMapper(),
                auth_service=auth_service_mock
            )
        ],
        auth_service=auth_service_mock,
        i18n_manager=i18n_manager,
        logger=logger
    ) as test_client:
        yield test_client


class TestFilesRoutes(RouteContract):
    # `download` and `upload` are covered separately: they need a stream / multipart body.
    ROUTES = [
        Route("GET", f"{URL}/", "get_list", [PermissionEnum.SERVER_FILES_VIEW],
              call_kwargs={"server_id": SERVER_ID, "dto": FilesGetListDto(path="/")},
              return_value=LISTING),
        Route("GET", f"{URL}/content", "get_content", [PermissionEnum.SERVER_FILES_VIEW],
              params={"path": "/server.properties"},
              call_kwargs={"server_id": SERVER_ID, "dto": FileGetContentDto(path="/server.properties")},
              return_value=CONTENT),
        Route("PUT", f"{URL}/content", "save_content", [PermissionEnum.SERVER_FILES_UPDATE],
              json={"path": "/server.properties", "content": "motd=New"},
              call_kwargs={
                  "server_id": SERVER_ID,
                  "dto": FileSaveContentDto(path="/server.properties", content="motd=New")
              },
              status=NO_CONTENT),
        Route("POST", f"{URL}/", "create", [PermissionEnum.SERVER_FILES_CREATE],
              json={"path": "/plugins", "type": "directory"},
              call_kwargs={
                  "server_id": SERVER_ID,
                  "dto": FileCreateDto(path="/plugins", type=FileTypeEnum.DIRECTORY, content=None)
              },
              status=NO_CONTENT),
        Route("POST", f"{URL}/move", "move", [PermissionEnum.SERVER_FILES_UPDATE],
              json={"paths": ["/a.txt"], "destination_path": "/backup"},
              call_kwargs={
                  "server_id": SERVER_ID,
                  "dto": FilesMoveDto(paths=["/a.txt"], destination_path="/backup")
              },
              status=NO_CONTENT),
        Route("POST", f"{URL}/rename", "rename", [PermissionEnum.SERVER_FILES_UPDATE],
              json={"path": "/a.txt", "name": "b.txt"},
              call_kwargs={
                  "server_id": SERVER_ID,
                  "dto": FileRenameDto(path="/a.txt", name="b.txt", overwrite=False)
              },
              status=NO_CONTENT),
        Route("POST", f"{URL}/duplicate", "duplicate", [PermissionEnum.SERVER_FILES_CREATE],
              json=["/a.txt", "/world"],
              call_kwargs={"server_id": SERVER_ID, "dto": FilesDuplicateDto(paths=["/a.txt", "/world"])},
              status=NO_CONTENT),
        Route("POST", f"{URL}/extract", "extract", [PermissionEnum.SERVER_FILES_EXTRACT],
              json={"path": "/mods.zip"},
              call_kwargs={
                  "server_id": SERVER_ID,
                  "dto": FilesExtractDto(path="/mods.zip", destination_path=None)
              },
              status=NO_CONTENT),
        Route("DELETE", f"{URL}/", "delete", [PermissionEnum.SERVER_FILES_DELETE],
              json=["/a.txt"],
              call_kwargs={"server_id": SERVER_ID, "dto": FilesDeleteDto(paths=["/a.txt"])},
              status=NO_CONTENT)
    ]


class TestListAndContent:
    def test_list_serializes_files_and_directories(self, client, login_as, files_service_mock):
        login_as(client)
        files_service_mock.get_list.return_value = LISTING

        response = client.get(f"{URL}/", params={"path": "/"})

        body = response.json()
        assert (body["total_files"], body["total_directories"]) == (1, 1)
        assert [(f["name"], f["type"]) for f in body["files"]] == [("world", "directory"), ("server.properties", "file")]
        assert body["files"][0]["size"] is None

    def test_content_requires_path(self, client, login_as, files_service_mock):
        login_as(client)

        response = client.get(f"{URL}/content")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert response.json() == {"message": "Path is required"}
        files_service_mock.get_content.assert_not_awaited()

    def test_content_returns_file_body(self, client, login_as, files_service_mock):
        login_as(client)
        files_service_mock.get_content.return_value = CONTENT

        response = client.get(f"{URL}/content", params={"path": "/server.properties"})

        assert response.json()["content"] == "motd=Cobalt"

    def test_path_traversal_rejected_by_service_returns_400(self, client, login_as, files_service_mock):
        login_as(client)
        files_service_mock.get_content.side_effect = ValidationError("Invalid path")

        response = client.get(f"{URL}/content", params={"path": "../../etc/passwd"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"message": "Invalid path"}

    def test_missing_file_returns_404(self, client, login_as, files_service_mock):
        login_as(client)
        files_service_mock.get_content.side_effect = NotFoundError("File not found")

        response = client.get(f"{URL}/content", params={"path": "/nope.txt"})

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestMutations:
    def test_create_with_unknown_type_returns_422(self, client, login_as, files_service_mock):
        login_as(client)

        response = client.post(f"{URL}/", json={"path": "/x", "type": "symlink"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        files_service_mock.create.assert_not_awaited()

    def test_rename_overwrite_flag_is_forwarded(self, client, login_as, files_service_mock):
        login_as(client)

        client.post(f"{URL}/rename", json={"path": "/a.txt", "name": "b.txt", "overwrite": True})

        assert files_service_mock.rename.await_args.kwargs["dto"].overwrite is True

    def test_rename_onto_existing_file_returns_409(self, client, login_as, files_service_mock):
        login_as(client)
        files_service_mock.rename.side_effect = ConflictError("File already exists")

        response = client.post(f"{URL}/rename", json={"path": "/a.txt", "name": "b.txt"})

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_extract_with_destination(self, client, login_as, files_service_mock):
        login_as(client)

        client.post(f"{URL}/extract", json={"path": "/mods.zip", "destination_path": "/mods"})

        files_service_mock.extract.assert_awaited_once_with(
            server_id=SERVER_ID,
            dto=FilesExtractDto(path="/mods.zip", destination_path="/mods")
        )

    def test_view_permission_cannot_delete(self, client, login_as, files_service_mock):
        login_as(client, permissions=[PermissionEnum.SERVER_FILES_VIEW])

        response = client.request("DELETE", f"{URL}/", json=["/a.txt"])

        assert response.status_code == status.HTTP_403_FORBIDDEN
        files_service_mock.delete.assert_not_awaited()


class TestUpload:
    def test_uploads_multipart_files(self, client, login_as, files_service_mock):
        login_as(client, permissions=[PermissionEnum.SERVER_FILES_UPLOAD])

        response = client.post(
            f"{URL}/upload",
            params={"path": "/plugins"},
            files=[
                ("files", ("a.jar", b"jar-a", "application/java-archive")),
                ("files", ("b.jar", b"jar-b", "application/java-archive"))
            ]
        )

        assert response.status_code == NO_CONTENT
        files_service_mock.upload.assert_awaited_once_with(
            server_id=SERVER_ID,
            dto=FilesUploadDto(path="/plugins", files=[("a.jar", b"jar-a"), ("b.jar", b"jar-b")])
        )

    def test_requires_upload_permission(self, client, login_as, files_service_mock):
        login_as(client, permissions=[PermissionEnum.SERVER_FILES_CREATE])

        response = client.post(
            f"{URL}/upload", params={"path": "/"}, files=[("files", ("a.txt", b"a", "text/plain"))]
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        files_service_mock.upload.assert_not_awaited()

    def test_without_files_returns_422(self, client, login_as, files_service_mock):
        login_as(client)

        response = client.post(f"{URL}/upload", params={"path": "/"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        files_service_mock.upload.assert_not_awaited()


class TestDownload:
    def test_streams_zip_archive(self, client, login_as, files_service_mock):
        login_as(client, permissions=[PermissionEnum.SERVER_FILES_DOWNLOAD])
        files_service_mock.download.return_value = _zip_stream()

        response = client.post(f"{URL}/download", json=["/world", "/server.properties"])

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/zip"
        assert response.headers["content-disposition"] == f"attachment; filename=server_{SERVER_ID}_files.zip"
        assert response.content == b"PK\x03\x04rest-of-archive"
        files_service_mock.download.assert_awaited_once_with(
            server_id=SERVER_ID,
            dto=FilesDownloadDto(paths=["/world", "/server.properties"])
        )

    def test_requires_download_permission(self, client, login_as, files_service_mock):
        login_as(client, permissions=[PermissionEnum.SERVER_FILES_VIEW])

        response = client.post(f"{URL}/download", json=["/world"])

        assert response.status_code == status.HTTP_403_FORBIDDEN
        files_service_mock.download.assert_not_awaited()
