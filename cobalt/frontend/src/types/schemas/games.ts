/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { SortDirection } from "@/types"

/**
 * Represents a paginated games list request.
 */
export interface GamesPageRequest {
  page?: number
  search?: string
  sort_field?: "id" | "name" | "loader_id" | "created_at" | "updated_at"
  sort_direction?: SortDirection
  limit?: number
}
