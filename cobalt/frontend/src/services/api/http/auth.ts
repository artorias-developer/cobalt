/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IHttpClient, IHttpAuthApiService } from "@/contracts"
import type { AuthLoginRequest, AuthChangeCredentialsRequest } from "@/types"

/**
 * API service for auth endpoints.
 */
export class HttpAuthApiService implements IHttpAuthApiService {
  private readonly prefix = "/api/v1/auth"
  private readonly client: IHttpClient

  constructor(client: IHttpClient) {
    this.client = client
  }

  /**
   * Authenticates a user and creates a session.
   *
   * Parameters:
   * - data: AuthLoginRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  async login(data: AuthLoginRequest): Promise<void> {
    return this.client.post<void>(`${this.prefix}/login`, data)
  }

  /**
   * Logs out the currently authenticated user.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>.
   */
  async logout(): Promise<void> {
    return this.client.post<void>(`${this.prefix}/logout`)
  }

  /**
   * Changes login and/or password for the currently authenticated user.
   *
   * Parameters:
   * - data: AuthChangeCredentialsRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  async changeCredentials(data: AuthChangeCredentialsRequest): Promise<void> {
    return this.client.patch<void>(`${this.prefix}/credentials`, data)
  }
}