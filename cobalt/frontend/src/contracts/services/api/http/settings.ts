/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { SettingsEntity, SettingsUpdateRequest } from "@/types"

/**
 * Interface for settings API service operations.
 * Defines contract for managing settings.
 * Implementation-agnostic - not tied to any specific HTTP client.
 */
export interface IHttpSettingsApiService {
  /**
   * Updates settings for the currently authenticated user.
   *
   * Parameters:
   * - data: SettingsUpdateRequest object.
   *
   * Returns:
   * - Promise<SettingsEntity>: Updated settings entity.
   */
  updateMe(data: SettingsUpdateRequest): Promise<SettingsEntity>

  /**
   * Clears application cached data.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>: Empty promise.
   */
  clearCache(): Promise<void>

  /**
   * Clears unused containers data.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>: Empty promise.
   */
  clearContainers(): Promise<void>
}