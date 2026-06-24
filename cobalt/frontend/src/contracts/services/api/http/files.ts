/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type {
  FileContentEntity,
  FilesListEntity,
  FilesListRequest,
  FileGetContentRequest,
  FileSaveContentRequest,
  FilesMoveRequest,
  FileRenameRequest,
  FilesDuplicateRequest,
  FilesDeleteRequest,
  FilesDownloadRequest,
  FileCreateRequest,
  FilesUploadRequest,
  FilesExtractRequest
} from "@/types"

/**
 * Interface for files API service operations.
 * Defines contract for managing server files.
 * Implementation-agnostic - not tied to any specific HTTP client.
 */
export interface IHttpFilesApiService {
  /**
   * Gets a list of entries in the given directory.
   *
   * Parameters:
   * - serverId: Server ID.
   * - params: FilesListRequest object.
   *
   * Returns:
   * - Promise<FilesListEntity>: List of files.
   */
  getList(serverId: number, params: FilesListRequest): Promise<FilesListEntity>

  /**
   * Gets the content of a specific file.
   *
   * Parameters:
   * - serverId: Server ID.
   * - params: FileGetContentRequest object.
   *
   * Returns:
   * - Promise<FileContentEntity>: File content entity.
   */
  getContent(serverId: number, params: FileGetContentRequest): Promise<FileContentEntity>

  /**
   * Saves the content of a specific file.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: FileSaveContentRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  saveContent(serverId: number, data: FileSaveContentRequest): Promise<void>

  /**
   * Creates a new file.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: FileCreateRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  create(serverId: number, data: FileCreateRequest): Promise<void>

  /**
   * Uploads one or multiple files to the given directory.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: FilesUploadRequest object.
   * - onProgress: Optional callback invoked with upload percent (0–100).
   *
   * Returns:
   * - Promise<void>.
   */
  upload(serverId: number, data: FilesUploadRequest, onProgress?: (percent: number) => void): Promise<void>

  /**
   * Downloads one or multiple files/directories as a zip archive.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: FilesDownloadRequest object.
   *
   * Returns:
   * - Promise<Blob>: Zip archive blob.
   */
  download(serverId: number, data: FilesDownloadRequest): Promise<Blob>

  /**
   * Moves one or multiple files/directories to the destination path.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: FilesMoveRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  move(serverId: number, data: FilesMoveRequest): Promise<void>

  /**
   * Renames a file or directory.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: FileRenameRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  rename(serverId: number, data: FileRenameRequest): Promise<void>

  /**
   * Duplicates one or multiple files/directories.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: FilesDuplicateRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  duplicate(serverId: number, data: FilesDuplicateRequest): Promise<void>

  /**
   * Extracts a ZIP archive to the destination path.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: FilesExtractRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  extract(serverId: number, data: FilesExtractRequest): Promise<void>

  /**
   * Deletes one or multiple files/directories.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: FilesDeleteRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  delete(serverId: number, data: FilesDeleteRequest): Promise<void>
}