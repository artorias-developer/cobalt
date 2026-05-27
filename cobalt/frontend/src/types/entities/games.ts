/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { LoaderEntity } from "@/types"

/**
 * Represents a game object.
 */
export interface GameEntity {
  id: number
  name: string
  loaders: LoaderEntity[]
  created_at: string
  updated_at: string
}

/**
 * Represents a paginated games page object.
 */
export interface GamesPageEntity {
  games: GameEntity[]
  total: number
  page: number
  pages: number
}
