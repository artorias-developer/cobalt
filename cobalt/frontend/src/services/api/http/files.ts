/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IHttpClient, IHttpFilesApiService } from "@/contracts"
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
 * API service for files endpoints.
 */
export class HttpFilesApiService implements IHttpFilesApiService {
  private readonly prefix = "/api/v1/servers"
  private readonly client: IHttpClient

  constructor(client: IHttpClient) {
    this.client = client
  }

  /**
   * Gets a list of entries in the given directory.
   *
   * Parameters:
   * - serverId: Server ID.
   * - params: FilesListRequest object.
   *
   * Returns:
   * - Promise<FilesListEntity>: Paginated list of files.
   */
  async getList(serverId: number, params: FilesListRequest): Promise<FilesListEntity> {
    return this.client.get<FilesListEntity>(`${this.prefix}/${serverId}/files/`, { params })
  }

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
  async getContent(serverId: number, params: FileGetContentRequest): Promise<FileContentEntity> {
    return this.client.get<FileContentEntity>(`${this.prefix}/${serverId}/files/content`, { params })
  }

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
  async saveContent(serverId: number, data: FileSaveContentRequest): Promise<void> {
    return this.client.put<void>(`${this.prefix}/${serverId}/files/content`, data)
  }

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
  async create(serverId: number, data: FileCreateRequest): Promise<void> {
    return this.client.post<void>(`${this.prefix}/${serverId}/files/`, data)
  }

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
  async upload(serverId: number, data: FilesUploadRequest, onProgress?: (percent: number) => void): Promise<void> {
    const formData = new FormData()

    for (const file of data.files) {
      formData.append("files", file)
    }

    return this.client.post<void>(`${this.prefix}/${serverId}/files/upload`, formData, {
      params: {
        path: data.path
      },
      headers: {
        "Content-Type": "multipart/form-data"
      },
      onUploadProgress: (e: ProgressEvent) => {
        if (onProgress && e.total) {
          onProgress(Math.round((e.loaded / e.total) * 100))
        }
      }
    })
  }

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
  async download(serverId: number, data: FilesDownloadRequest): Promise<Blob> {
    return this.client.post<Blob>(`${this.prefix}/${serverId}/files/download`, data.paths, {
      responseType: "blob"
    })
  }

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
  async move(serverId: number, data: FilesMoveRequest): Promise<void> {
    return this.client.post<void>(`${this.prefix}/${serverId}/files/move`, data)
  }

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
  async rename(serverId: number, data: FileRenameRequest): Promise<void> {
    return this.client.post<void>(`${this.prefix}/${serverId}/files/rename`, data)
  }

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
  async duplicate(serverId: number, data: FilesDuplicateRequest): Promise<void> {
    return this.client.post<void>(`${this.prefix}/${serverId}/files/duplicate`, data.paths)
  }

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
  async extract(serverId: number, data: FilesExtractRequest): Promise<void> {
    return this.client.post<void>(`${this.prefix}/${serverId}/files/extract`, data)
  }

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
  async delete(serverId: number, data: FilesDeleteRequest): Promise<void> {
    return this.client.delete<void>(`${this.prefix}/${serverId}/files/`, { data: data.paths })
  }
}