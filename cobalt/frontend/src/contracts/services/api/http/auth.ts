/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { AuthLoginRequest, AuthChangeCredentialsRequest } from "@/types"

/**
 * Interface for auth API service operations.
 * Defines contract for authentication.
 * Implementation-agnostic - not tied to any specific HTTP client.
 */
export interface IHttpAuthApiService {
  /**
   * Authenticates a user and creates a session.
   *
   * Parameters:
   * - data: AuthLoginRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  login(data: AuthLoginRequest): Promise<void>

  /**
   * Logs out the currently authenticated user.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>.
   */
  logout(): Promise<void>

  /**
   * Changes login and/or password for the currently authenticated user.
   *
   * Parameters:
   * - data: AuthChangeCredentialsRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  changeCredentials(data: AuthChangeCredentialsRequest): Promise<void>
}