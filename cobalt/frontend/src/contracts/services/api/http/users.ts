/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type {
  UserEntity,
  UserMeEntity,
  UsersPageEntity,
  UsersPageRequest,
  UserCreateRequest,
  UserUpdateRequest
} from "@/types"

/**
 * Interface for users API service operations.
 * Defines contract for managing users.
 * Implementation-agnostic - not tied to any specific HTTP client.
 */
export interface IHttpUsersApiService {
  /**
   * Gets the currently authenticated user.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<UserMeEntity>: Current user entity.
   */
  getMe(): Promise<UserMeEntity>

  /**
   * Gets a paginated list of users.
   *
   * Parameters:
   * - params: UsersPageRequest object.
   *
   * Returns:
   * - Promise<UsersPageEntity>: Paginated list of users.
   */
  getPage(params: UsersPageRequest): Promise<UsersPageEntity>

  /**
   * Gets an existing user.
   *
   * Parameters:
   * - userId: User ID.
   *
   * Returns:
   * - Promise<UserEntity>: User entity.
   */
  getOne(userId: number): Promise<UserEntity>

  /**
   * Creates a new user.
   *
   * Parameters:
   * - data: UserCreateRequest object.
   *
   * Returns:
   * - Promise<UserEntity>: Created user entity.
   */
  createOne(data: UserCreateRequest): Promise<UserEntity>

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
  updateOne(userId: number, data: UserUpdateRequest): Promise<UserEntity>

  /**
   * Deletes an existing user.
   *
   * Parameters:
   * - userId: User ID.
   *
   * Returns:
   * - Promise<void>.
   */
  deleteOne(userId: number): Promise<void>

  /**
   * Deletes multiple existing users.
   *
   * Parameters:
   * - ids: List of user IDs.
   *
   * Returns:
   * - Promise<void>.
   */
  deleteMany(ids: number[]): Promise<void>
}