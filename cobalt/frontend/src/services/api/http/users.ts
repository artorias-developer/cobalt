/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IHttpClient, IHttpUsersApiService } from "@/contracts"
import type {
  UserEntity,
  UserMeEntity,
  UsersPageEntity,
  UsersPageRequest,
  UserCreateRequest,
  UserUpdateRequest
} from "@/types"

/**
 * API service for users endpoints.
 */
export class HttpUsersApiService implements IHttpUsersApiService {
  private readonly prefix = "/api/v1/users"
  private readonly client: IHttpClient

  constructor(client: IHttpClient) {
    this.client = client
  }

  /**
   * Gets the currently authenticated user.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<UserMeEntity>: Current user entity.
   */
  async getMe(): Promise<UserMeEntity> {
    return this.client.get<UserMeEntity>(`${this.prefix}/me`)
  }

  /**
   * Gets a paginated list of users.
   *
   * Parameters:
   * - params: UsersPageRequest object.
   *
   * Returns:
   * - Promise<UsersPageEntity>: Paginated list of users.
   */
  async getPage(params: UsersPageRequest): Promise<UsersPageEntity> {
    return this.client.get<UsersPageEntity>(`${this.prefix}/`, { params })
  }

  /**
   * Gets an existing user.
   *
   * Parameters:
   * - userId: User ID.
   *
   * Returns:
   * - Promise<UserEntity>: User entity.
   */
  async getOne(userId: number): Promise<UserEntity> {
    return this.client.get<UserEntity>(`${this.prefix}/${userId}`)
  }

  /**
   * Creates a new user.
   *
   * Parameters:
   * - data: UserCreateRequest object.
   *
   * Returns:
   * - Promise<UserEntity>: Created user entity.
   */
  async createOne(data: UserCreateRequest): Promise<UserEntity> {
    return this.client.post<UserEntity>(`${this.prefix}/`, data)
  }

  /**
   * Updates an existing user.
   *
   * Parameters:
   * - userId: User ID.
   * - data: UserUpdateRequest object.
   *
   * Returns:
   * - Promise<UserEntity>: Updated user entity.
   */
  async updateOne(userId: number, data: UserUpdateRequest): Promise<UserEntity> {
    return this.client.patch<UserEntity>(`${this.prefix}/${userId}`, data)
  }

  /**
   * Deletes an existing user.
   *
   * Parameters:
   * - userId: User ID.
   *
   * Returns:
   * - Promise<void>.
   */
  async deleteOne(userId: number): Promise<void> {
    return this.client.delete<void>(`${this.prefix}/${userId}`)
  }

  /**
   * Deletes multiple existing users.
   *
   * Parameters:
   * - ids: List of user IDs.
   *
   * Returns:
   * - Promise<void>.
   */
  async deleteMany(ids: number[]): Promise<void> {
    return this.client.delete<void>(`${this.prefix}/batch`, { data: ids })
  }
}