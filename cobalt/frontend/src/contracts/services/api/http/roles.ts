/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type {
  RoleEntity,
  RolesPageEntity,
  RolesPageRequest,
  RoleCreateRequest,
  RoleUpdateRequest
} from "@/types"

/**
 * Interface for roles API service operations.
 * Defines contract for managing roles.
 * Implementation-agnostic - not tied to any specific HTTP client.
 */
export interface IHttpRolesApiService {
  /**
   * Gets a paginated list of roles.
   *
   * Parameters:
   * - params: RolesPageRequest object.
   *
   * Returns:
   * - Promise<RolesPageEntity>: Paginated list of roles.
   */
  getPage(params: RolesPageRequest): Promise<RolesPageEntity>

  /**
   * Gets an existing role.
   *
   * Parameters:
   * - roleId: Role ID.
   *
   * Returns:
   * - Promise<RoleEntity>: Role entity.
   */
  getOne(roleId: number): Promise<RoleEntity>

  /**
   * Creates a new role.
   *
   * Parameters:
   * - data: RoleCreateRequest object.
   *
   * Returns:
   * - Promise<RoleEntity>: Created role entity.
   */
  createOne(data: RoleCreateRequest): Promise<RoleEntity>

  /**
   * Updates an existing role.
   *
   * Parameters:
   * - roleId: Role ID.
   * - data: RoleUpdateRequest object.
   *
   * Returns:
   * - Promise<RoleEntity>: Updated role entity.
   */
  updateOne(roleId: number, data: RoleUpdateRequest): Promise<RoleEntity>

  /**
   * Deletes an existing role.
   *
   * Parameters:
   * - roleId: Role ID.
   *
   * Returns:
   * - Promise<void>.
   */
  deleteOne(roleId: number): Promise<void>

  /**
   * Deletes multiple existing roles.
   *
   * Parameters:
   * - ids: List of role IDs.
   *
   * Returns:
   * - Promise<void>.
   */
  deleteMany(ids: number[]): Promise<void>
}