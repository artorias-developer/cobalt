/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type {
  GameEntity,
  LoaderEntity,
  AttributeEntity,
  ServerStatusEnum
} from "@/types"

/**
 * Represents a server object.
 */
export interface ServerEntity {
  id: number
  name: string
  version: string
  game: GameEntity
  loader: LoaderEntity
  attributes: AttributeEntity[]
  status: ServerStatusEnum
  created_at: string
  updated_at: string
}

/**
 * Represents a paginated servers page object.
 */
export interface ServersPageEntity {
  servers: ServerEntity[]
  total: number
  page: number
  pages: number
}

/**
 * Represents a server status object.
 */
export interface ServerStatusEntity {
  running: boolean
  port: number | null
}