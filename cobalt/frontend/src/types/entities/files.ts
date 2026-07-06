/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Represents a file or directory entry.
 */
export interface FileEntity {
  name: string
  path: string
  type: "file" | "directory"
  format: string | null
  size: number | null
  modified_at: string
}

/**
 * Represents a file list response.
 */
export interface FilesListEntity {
  files: FileEntity[]
  path: string
  total_files: number
  total_directories: number
}

/**
 * Represents a file content response.
 */
export interface FileContentEntity {
  path: string
  name: string
  format: string | null
  size: number
  content: string
  modified_at: string
}