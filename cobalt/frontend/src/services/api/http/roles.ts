/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IHttpClient, IHttpRolesApiService } from "@/contracts"
import type {
  RoleEntity,
  RolesPageEntity,
  RolesPageRequest,
  RoleCreateRequest,
  RoleUpdateRequest
} from "@/types"

/**
 * API service for roles endpoints.
 */
export class HttpRolesApiService implements IHttpRolesApiService {
  private readonly prefix = "/api/v1/roles"
  private readonly client: IHttpClient

  constructor(client: IHttpClient) {
    this.client = client
  }

  /**
   * Gets a paginated list of roles.
   *
   * Parameters:
   * - params: RolesPageRequest object.
   *
   * Returns:
   * - Promise<RolesPageEntity>: Paginated list of roles.
   */
  async getPage(params: RolesPageRequest): Promise<RolesPageEntity> {
    return this.client.get<RolesPageEntity>(`${this.prefix}/`, { params })
  }

  /**
   * Gets an existing role.
   *
   * Parameters:
   * - roleId: Role ID.
   *
   * Returns:
   * - Promise<RoleEntity>: Role entity.
   */
  async getOne(roleId: number): Promise<RoleEntity> {
    return this.client.get<RoleEntity>(`${this.prefix}/${roleId}`)
  }

  /**
   * Creates a new role.
   *
   * Parameters:
   * - data: RoleCreateRequest object.
   *
   * Returns:
   * - Promise<RoleEntity>: Created role entity.
   */
  async createOne(data: RoleCreateRequest): Promise<RoleEntity> {
    return this.client.post<RoleEntity>(`${this.prefix}/`, data)
  }

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
  async updateOne(roleId: number, data: RoleUpdateRequest): Promise<RoleEntity> {
    return this.client.patch<RoleEntity>(`${this.prefix}/${roleId}`, data)
  }

  /**
   * Deletes an existing role.
   *
   * Parameters:
   * - roleId: Role ID.
   *
   * Returns:
   * - Promise<void>.
   */
  async deleteOne(roleId: number): Promise<void> {
    return this.client.delete<void>(`${this.prefix}/${roleId}`)
  }

  /**
   * Deletes multiple existing roles.
   *
   * Parameters:
   * - ids: List of role IDs.
   *
   * Returns:
   * - Promise<void>.
   */
  async deleteMany(ids: number[]): Promise<void> {
    return this.client.delete<void>(`${this.prefix}/batch`, { data: ids })
  }
}