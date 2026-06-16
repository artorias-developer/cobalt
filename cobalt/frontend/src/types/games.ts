/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

export type GameLoaderModule = {
  displayName: string
}

export type GameModule = {
  displayName: string
  icon: string
  loaders: Record<string, GameLoaderModule>
  sort_number: number
}

export type GameModulesMap = Record<string, GameModule>