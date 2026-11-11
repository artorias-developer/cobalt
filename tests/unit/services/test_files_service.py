#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
FilesService works on the real filesystem, so these tests run inside pytest's `tmp_path`.
Only the archives manager is mocked.
"""

from pathlib import Path
from unittest.mock import MagicMock, create_autospec, sentinel

import pytest

from domain.enums import FileTypeEnum
from domain.exceptions import ConflictError, NotFoundError, PermissionsError
from application.contracts.managers import AbstractArchivesManager
from application.services.files import FilesService
from application.dtos import (
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


SERVER_ID = 1


@pytest.fixture
def archives_manager() -> MagicMock:
    return create_autospec(AbstractArchivesManager, instance=True)


@pytest.fixture
def root(tmp_path) -> Path:
    root = tmp_path / "containers" / f"cobalt_server_{SERVER_ID}"
    (root / "world" / "region").mkdir(parents=True)
    (root / "server.properties").write_text("motd=Cobalt\n")
    (root / "world" / "level.dat").write_bytes(b"\x00\x01")
    (root / "Banned.json").write_text("[]")
    return root


@pytest.fixture
def outside(tmp_path) -> Path:
    secret = tmp_path / "secret.txt"
    secret.write_text("do not leak")
    return secret


@pytest.fixture
def service(tmp_path, root, archives_manager) -> FilesService:
    return FilesService(app_containers_dir=tmp_path / "containers", archives_manager=archives_manager)


TRAVERSAL_PATHS = ["../secret.txt", "/../../secret.txt", "world/../../secret.txt"]


class TestPathSafety:
    @pytest.mark.parametrize("path", TRAVERSAL_PATHS)
    async def test_traversal_is_rejected_for_reads(self, service, path):
        with pytest.raises(PermissionsError):
            await service.get_content(SERVER_ID, FileGetContentDto(path=path))

    @pytest.mark.parametrize("path", TRAVERSAL_PATHS)
    async def test_traversal_is_rejected_for_writes(self, service, outside, path):
        with pytest.raises(PermissionsError):
            await service.save_content(SERVER_ID, FileSaveContentDto(path=path, content="pwned"))

        assert outside.read_text() == "do not leak"

    async def test_symlink_escaping_root_is_rejected(self, service, root, outside):
        (root / "link.txt").symlink_to(outside)

        with pytest.raises(PermissionsError):
            await service.get_content(SERVER_ID, FileGetContentDto(path="/link.txt"))

    async def test_other_server_is_not_reachable(self, service, tmp_path):
        other = tmp_path / "containers" / "cobalt_server_2"
        other.mkdir()
        (other / "ops.json").write_text("[]")

        with pytest.raises(PermissionsError):
            await service.get_content(SERVER_ID, FileGetContentDto(path="../cobalt_server_2/ops.json"))

    @pytest.mark.parametrize("call", [
        lambda s: s.delete(SERVER_ID, FilesDeleteDto(paths=["/"])),
        lambda s: s.create(SERVER_ID, FileCreateDto(path="/", type=FileTypeEnum.DIRECTORY)),
        lambda s: s.rename(SERVER_ID, FileRenameDto(path="/", name="x"))
    ])
    async def test_root_itself_cannot_be_modified(self, service, root, call):
        with pytest.raises(PermissionsError):
            await call(service)

        assert root.exists()


class TestGetList:
    async def test_directories_first_then_case_insensitive_names(self, service):
        result = await service.get_list(SERVER_ID, FilesGetListDto(path="/"))

        assert [(f.name, f.type) for f in result.files] == [
            ("world", FileTypeEnum.DIRECTORY),
            ("Banned.json", FileTypeEnum.FILE),
            ("server.properties", FileTypeEnum.FILE)
        ]
        assert (result.total_files, result.total_directories) == (2, 1)

    async def test_file_metadata(self, service):
        result = await service.get_list(SERVER_ID, FilesGetListDto(path="/"))
        by_name = {f.name: f for f in result.files}

        assert by_name["server.properties"].path == "/server.properties"
        assert by_name["server.properties"].format == "properties"
        assert by_name["server.properties"].size == len("motd=Cobalt\n")
        assert by_name["world"].size is None and by_name["world"].format is None

    async def test_nested_paths_are_relative_to_root(self, service):
        result = await service.get_list(SERVER_ID, FilesGetListDto(path="/world"))

        assert sorted(f.path for f in result.files) == ["/world/level.dat", "/world/region"]

    async def test_missing_directory(self, service):
        with pytest.raises(NotFoundError):
            await service.get_list(SERVER_ID, FilesGetListDto(path="/nope"))

    async def test_file_is_not_a_directory(self, service):
        with pytest.raises(NotFoundError):
            await service.get_list(SERVER_ID, FilesGetListDto(path="/server.properties"))


class TestContent:
    async def test_reads_text_file(self, service):
        result = await service.get_content(SERVER_ID, FileGetContentDto(path="/server.properties"))

        assert result.content == "motd=Cobalt\n"
        assert (result.path, result.name, result.format) == ("/server.properties", "server.properties", "properties")

    async def test_binary_content_is_replaced_not_crashing(self, service, root):
        (root / "blob.bin").write_bytes(b"\xff\xfe\x00ok")

        result = await service.get_content(SERVER_ID, FileGetContentDto(path="/blob.bin"))

        assert result.content.endswith("ok")

    async def test_rejects_files_over_limit(self, service, root):
        (root / "huge.log").write_bytes(b"x" * (FilesService._MAX_FILE_READ_SIZE + 1))

        with pytest.raises(ConflictError):
            await service.get_content(SERVER_ID, FileGetContentDto(path="/huge.log"))

    async def test_directory_is_not_a_file(self, service):
        with pytest.raises(NotFoundError):
            await service.get_content(SERVER_ID, FileGetContentDto(path="/world"))

    async def test_save_overwrites_and_truncates(self, service, root):
        await service.save_content(SERVER_ID, FileSaveContentDto(path="/server.properties", content="a=1"))

        assert (root / "server.properties").read_text() == "a=1"

    async def test_save_does_not_create_missing_file(self, service, root):
        with pytest.raises(NotFoundError):
            await service.save_content(SERVER_ID, FileSaveContentDto(path="/new.txt", content="x"))

        assert not (root / "new.txt").exists()


class TestCreate:
    async def test_creates_file_with_parents(self, service, root):
        await service.create(SERVER_ID, FileCreateDto(path="/plugins/cfg/a.yml", type=FileTypeEnum.FILE, content="k: v"))

        assert (root / "plugins" / "cfg" / "a.yml").read_text() == "k: v"

    async def test_creates_empty_file_without_content(self, service, root):
        await service.create(SERVER_ID, FileCreateDto(path="/empty.txt", type=FileTypeEnum.FILE))

        assert (root / "empty.txt").read_text() == ""

    async def test_creates_directory(self, service, root):
        await service.create(SERVER_ID, FileCreateDto(path="/mods", type=FileTypeEnum.DIRECTORY))

        assert (root / "mods").is_dir()

    @pytest.mark.parametrize(("path", "file_type"), [
        ("/server.properties", FileTypeEnum.FILE),
        ("/world", FileTypeEnum.DIRECTORY),
        ("/server.properties/child", FileTypeEnum.FILE)
    ])
    async def test_existing_path_conflicts(self, service, root, path, file_type):
        with pytest.raises(ConflictError):
            await service.create(SERVER_ID, FileCreateDto(path=path, type=file_type, content="x"))

        assert (root / "server.properties").read_text() == "motd=Cobalt\n"


class TestUpload:
    async def test_writes_all_files(self, service, root):
        await service.upload(SERVER_ID, FilesUploadDto(path="/world", files=[("a.bin", b"A"), ("b.bin", b"B")]))

        assert (root / "world" / "a.bin").read_bytes() == b"A"
        assert (root / "world" / "b.bin").read_bytes() == b"B"

    @pytest.mark.parametrize("name", ["../evil.sh", "sub/evil.sh", "..", ".", "", "a\\b", "nul\0"])
    async def test_rejects_unsafe_names_before_writing_anything(self, service, root, name):
        with pytest.raises(PermissionsError):
            await service.upload(SERVER_ID, FilesUploadDto(path="/", files=[("ok.txt", b"1"), (name, b"2")]))

        assert not (root / "ok.txt").exists()

    async def test_destination_must_be_directory(self, service):
        with pytest.raises(NotFoundError):
            await service.upload(SERVER_ID, FilesUploadDto(path="/server.properties", files=[("a", b"")]))

    async def test_name_of_existing_directory_conflicts(self, service):
        with pytest.raises(ConflictError):
            await service.upload(SERVER_ID, FilesUploadDto(path="/", files=[("world", b"x")]))


class TestMoveRenameDuplicate:
    async def test_move_into_directory(self, service, root):
        await service.move(SERVER_ID, FilesMoveDto(paths=["/Banned.json"], destination_path="/world"))

        assert (root / "world" / "Banned.json").exists()
        assert not (root / "Banned.json").exists()

    async def test_move_name_collision(self, service, root):
        (root / "world" / "Banned.json").write_text("other")

        with pytest.raises(ConflictError):
            await service.move(SERVER_ID, FilesMoveDto(paths=["/Banned.json"], destination_path="/world"))

        assert (root / "Banned.json").read_text() == "[]"

    async def test_move_to_missing_destination(self, service):
        with pytest.raises(NotFoundError):
            await service.move(SERVER_ID, FilesMoveDto(paths=["/Banned.json"], destination_path="/nope"))

    async def test_move_missing_source(self, service):
        with pytest.raises(NotFoundError):
            await service.move(SERVER_ID, FilesMoveDto(paths=["/nope"], destination_path="/world"))

    async def test_rename(self, service, root):
        await service.rename(SERVER_ID, FileRenameDto(path="/Banned.json", name="banned-players.json"))

        assert (root / "banned-players.json").read_text() == "[]"

    async def test_rename_to_existing_without_overwrite_conflicts(self, service, root):
        with pytest.raises(ConflictError):
            await service.rename(SERVER_ID, FileRenameDto(path="/Banned.json", name="server.properties"))

        assert (root / "server.properties").read_text() == "motd=Cobalt\n"

    async def test_rename_with_overwrite_replaces_file(self, service, root):
        await service.rename(SERVER_ID, FileRenameDto(path="/Banned.json", name="server.properties", overwrite=True))

        assert (root / "server.properties").read_text() == "[]"
        assert not (root / "Banned.json").exists()

    async def test_overwrite_never_replaces_directory(self, service, root):
        with pytest.raises(ConflictError):
            await service.rename(SERVER_ID, FileRenameDto(path="/Banned.json", name="world", overwrite=True))

        assert (root / "world" / "level.dat").exists()

    @pytest.mark.parametrize("name", ["../escape.json", "a/b", ".."])
    async def test_rename_rejects_unsafe_names(self, service, name):
        with pytest.raises(PermissionsError):
            await service.rename(SERVER_ID, FileRenameDto(path="/Banned.json", name=name))

    async def test_rename_to_same_name_is_noop(self, service, root):
        await service.rename(SERVER_ID, FileRenameDto(path="/Banned.json", name="Banned.json"))

        assert (root / "Banned.json").exists()

    async def test_duplicate_generates_unique_names(self, service, root):
        await service.duplicate(SERVER_ID, FilesDuplicateDto(paths=["/Banned.json"]))
        await service.duplicate(SERVER_ID, FilesDuplicateDto(paths=["/Banned.json"]))
        await service.duplicate(SERVER_ID, FilesDuplicateDto(paths=["/world"]))

        assert (root / "Banned_copy.json").read_text() == "[]"
        assert (root / "Banned_copy_1.json").exists()
        assert (root / "world_copy" / "level.dat").read_bytes() == b"\x00\x01"


class TestDeleteDownloadExtract:
    async def test_delete_files_and_directories(self, service, root):
        await service.delete(SERVER_ID, FilesDeleteDto(paths=["/world", "/Banned.json"]))

        assert not (root / "world").exists()
        assert not (root / "Banned.json").exists()
        assert (root / "server.properties").exists()

    async def test_delete_validates_all_paths_first(self, service, root):
        with pytest.raises(NotFoundError):
            await service.delete(SERVER_ID, FilesDeleteDto(paths=["/Banned.json", "/nope"]))

        assert (root / "Banned.json").exists()

    async def test_download_streams_resolved_paths(self, service, root, archives_manager):
        archives_manager.stream_zip.return_value = sentinel.stream

        result = await service.download(SERVER_ID, FilesDownloadDto(paths=["/world", "/server.properties"]))

        assert result is sentinel.stream
        archives_manager.stream_zip.assert_awaited_once_with(
            paths=[(root / "world").resolve(), (root / "server.properties").resolve()]
        )

    async def test_download_missing_path(self, service, archives_manager):
        with pytest.raises(NotFoundError):
            await service.download(SERVER_ID, FilesDownloadDto(paths=["/nope"]))

        archives_manager.stream_zip.assert_not_awaited()

    async def test_extract_defaults_to_archive_directory(self, service, root, archives_manager):
        (root / "world" / "mods.zip").write_bytes(b"PK")

        await service.extract(SERVER_ID, FilesExtractDto(path="/world/mods.zip"))

        archives_manager.extract_zip.assert_awaited_once_with(
            source=(root / "world" / "mods.zip").resolve(),
            destination=(root / "world").resolve()
        )

    async def test_extract_to_destination(self, service, root, archives_manager):
        (root / "mods.zip").write_bytes(b"PK")

        await service.extract(SERVER_ID, FilesExtractDto(path="/mods.zip", destination_path="/world"))

        assert archives_manager.extract_zip.await_args.kwargs["destination"] == (root / "world").resolve()

    async def test_extract_destination_outside_root_rejected(self, service, root, archives_manager):
        (root / "mods.zip").write_bytes(b"PK")

        with pytest.raises(PermissionsError):
            await service.extract(SERVER_ID, FilesExtractDto(path="/mods.zip", destination_path="../.."))

        archives_manager.extract_zip.assert_not_awaited()

    @pytest.mark.parametrize(("path", "destination"), [
        ("/nope.zip", None),
        ("/world", None),
        ("/server.properties", "/Banned.json")
    ])
    async def test_extract_invalid_paths(self, service, archives_manager, path, destination):
        with pytest.raises(NotFoundError):
            await service.extract(SERVER_ID, FilesExtractDto(path=path, destination_path=destination))

        archives_manager.extract_zip.assert_not_awaited()
