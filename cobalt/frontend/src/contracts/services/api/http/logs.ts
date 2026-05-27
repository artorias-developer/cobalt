/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { LogEntity } from "@/types"

/**
 * Interface for logs API service operations.
 * Defines contract for fetching host and server logs.
 * Implementation-agnostic - not tied to any specific HTTP client.
 */
export interface IHttpLogsApiService {
  /**
   * Gets all host log values.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<LogEntity[]>: List of host logs.
   */
  getHostAll(): Promise<LogEntity[]>

  /**
   * Gets all log values for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<LogEntity[]>: List of server logs.
   */
  getServerAll(serverId: number): Promise<LogEntity[]>
}