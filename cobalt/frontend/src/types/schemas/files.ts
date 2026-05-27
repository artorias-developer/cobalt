/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { FileType } from "@/types"

/**
 * Represents a files list request.
 */
export interface FilesListRequest {
  path: string
}

/**
 * Represents a file content request.
 */
export interface FileGetContentRequest {
  path: string
}

/**
 * Represents a file save content request.
 */
export interface FileSaveContentRequest {
  path: string
  content: string
}

/**
 * Represents a files move request.
 */
export interface FilesMoveRequest {
  paths: string[]
  destination_path: string
}

/**
 * Represents a file rename request.
 */
export interface FileRenameRequest {
  path: string
  name: string
}

/**
 * Represents a files duplicate request.
 */
export interface FilesDuplicateRequest {
  paths: string[]
}

/**
 * Represents a files delete request.
 */
export interface FilesDeleteRequest {
  paths: string[]
}

/**
 * Represents a files download request.
 */
export interface FilesDownloadRequest {
  paths: string[]
}

/**
 * Represents a file create request.
 */
export interface FileCreateRequest {
  path: string
  content?: string
  type: FileType
}

/**
 * Represents a files upload request.
 */
export interface FilesUploadRequest {
  path: string
  files: File[]
}

/**
 * Represents a files extract request.
 */
export interface FilesExtractRequest {
  path: string
  destination_path?: string
}