/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { SortDirection } from "@/types"

/**
 * Represents a paginated users list request.
 */
export interface UsersPageRequest {
  page?: number
  search?: string
  sort_field?: "id" | "login" | "role_id" | "created_at" | "updated_at"
  sort_direction?: SortDirection
  limit?: number
}

/**
 * Represents a user create request.
 */
export interface UserCreateRequest {
  login: string
  password: string
  role_id: number
}

/**
 * Represents a user update request.
 */
export interface UserUpdateRequest {
  login?: string
  password?: string
  role_id?: number
}