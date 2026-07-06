/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Represents a loader object.
 */
export interface LoaderEntity {
  id: number
  game_id: number
  name: string
  versions: string[]
  created_at: string
  updated_at: string
}