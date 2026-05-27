/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

export type BlockHeaderSize = "small" | "large"
export type ServerBlockMode = "server" | "empty"
export type UniversalBlockMode = "host" | "server" | "empty"

export type InfoField = {
  label: string
  value: string | null
  copyable?: boolean
}
