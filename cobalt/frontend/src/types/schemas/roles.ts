/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { PermissionsEnum, type SortDirection } from "@/types"

/**
 * Represents a paginated roles list request.
 */
export interface RolesPageRequest {
  page?: number
  search?: string
  sort_field?: "id" | "name" | "created_at" | "updated_at"
  sort_direction?: SortDirection
  limit?: number
}

/**
 * Represents a role create request.
 */
export interface RoleCreateRequest {
  name: string
  permissions: PermissionsEnum[]
}

/**
 * Represents a role update request.
 */
export interface RoleUpdateRequest {
  name?: string
  permissions?: PermissionsEnum[]
}