/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IHttpClient, IHttpSettingsApiService } from "@/contracts"
import type { SettingsEntity, SettingsUpdateRequest } from "@/types"

/**
 * API service for settings endpoints.
 */
export class HttpSettingsApiService implements IHttpSettingsApiService {
  private readonly prefix = "/api/v1/settings"
  private readonly client: IHttpClient

  constructor(client: IHttpClient) {
    this.client = client
  }

  /**
   * Updates settings for the currently authenticated user.
   *
   * Parameters:
   * - data: SettingsUpdateRequest object.
   *
   * Returns:
   * - Promise<SettingsEntity>: Updated settings entity.
   */
  async updateMe(data: SettingsUpdateRequest): Promise<SettingsEntity> {
    return this.client.patch<SettingsEntity>(`${this.prefix}/me`, data)
  }

  /**
   * Clears application cached data.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>: Empty promise.
   */
  async clearCache(): Promise<void> {
    return this.client.delete<void>(`${this.prefix}/cache`)
  }

  /**
   * Clears unused containers data.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>: Empty promise.
   */
  async clearContainers(): Promise<void> {
    return this.client.delete<void>(`${this.prefix}/containers`)
  }
}