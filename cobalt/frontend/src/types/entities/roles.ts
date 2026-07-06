/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { PermissionEnum } from "@/types"

/**
 * Represents a role object.
 */
export interface RoleEntity {
  id: number
  name: string
  permissions: PermissionEnum[]
  created_at: string
  updated_at: string
}

/**
 * Represents a paginated roles page object.
 */
export interface RolesPageEntity {
  roles: RoleEntity[]
  total: number
  page: number
  pages: number
}
