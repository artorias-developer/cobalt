/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IHttpClient, IHttpLogsApiService } from "@/contracts"
import type { LogEntity } from "@/types"

/**
 * API service for logs endpoints.
 * Covers host and per-server logs.
 */
export class HttpLogsApiService implements IHttpLogsApiService {
  private readonly prefix = "/api/v1/logs"
  private readonly client: IHttpClient

  constructor(client: IHttpClient) {
    this.client = client
  }

  /**
   * Gets all host log values.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<LogEntity[]>: List of host logs.
   */
  async getHostAll(): Promise<LogEntity[]> {
    return this.client.get<LogEntity[]>(`${this.prefix}/host`)
  }

  /**
   * Gets all log values for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<LogEntity[]>: List of server logs.
   */
  async getServerAll(serverId: number): Promise<LogEntity[]> {
    return this.client.get<LogEntity[]>(`${this.prefix}/servers/${serverId}`)
  }
}