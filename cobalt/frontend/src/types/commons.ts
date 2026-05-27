/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

export type Color = "gray" | "red" | "blue" | "green" | "yellow"
export type SortDirection = "asc" | "desc"
export type FileType = "file" | "directory"

export type Tag = {
  label?: string
  class?: string
}

export interface FileTypeEntry {
  icon: string
  language?: string
}