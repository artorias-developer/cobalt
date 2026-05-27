/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { RoleEntity, SettingsEntity } from "@/types"

/**
 * Represents a user object.
 */
export interface UserEntity {
  id: number
  login: string
  role: RoleEntity
  created_at: string
  updated_at: string
}

/**
 * Represents the currently authenticated user object.
 */
export interface UserMeEntity {
  id: number
  login: string
  role: RoleEntity
  settings: SettingsEntity
  created_at: string
  updated_at: string
}

/**
 * Represents a paginated users page object.
 */
export interface UsersPageEntity {
  users: UserEntity[]
  total: number
  page: number
  pages: number
}