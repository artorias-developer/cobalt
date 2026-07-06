/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { SortDirection } from "@/types"

/**
 * Represents a paginated servers list request.
 */
export interface ServersPageRequest {
  page?: number
  search?: string
  sort_field?: "id" | "name" | "game_id" | "loader_id" | "version" | "created_at" | "updated_at"
  sort_direction?: SortDirection
  limit?: number
}

/**
 * Represents a server create request.
 */
export interface ServerCreateRequest {
  name: string
  game_id: number
  loader_id: number
  version: string
}

/**
 * Represents a server update request.
 */
export interface ServerUpdateRequest {
  name?: string
}

/**
 * Represents a server execute request.
 */
export interface ServerExecuteRequest {
  command: string
}