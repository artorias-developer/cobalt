/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { PermissionsEnum } from "@/types"

/**
 * Represents a role object.
 */
export interface RoleEntity {
  id: number
  name: string
  permissions: PermissionsEnum[]
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
