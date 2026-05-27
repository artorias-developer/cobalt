/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IHttpClient, IHttpMetricsApiService } from "@/contracts"
import type { DiskMetricsEntity, MetricEntity } from "@/types"

/**
 * API service for metrics endpoints.
 * Covers host and per-server CPU, RAM, and disk metrics.
 */
export class HttpMetricsApiService implements IHttpMetricsApiService {
  private readonly prefix = "/api/v1/metrics"
  private readonly client: IHttpClient

  constructor(client: IHttpClient) {
    this.client = client
  }

  /**
   * Gets host disk usage metrics.
   *
   * Parameters:
   * - refresh: If true, bypasses cache and fetches fresh data (default: false).
   *
   * Returns:
   * - Promise<DiskMetricsEntity>: Host disk metrics.
   */
  async getHostDisk(refresh: boolean = false): Promise<DiskMetricsEntity> {
    return this.client.get<DiskMetricsEntity>(`${this.prefix}/host/disk`, {
      params: { refresh }
    })
  }

  /**
   * Gets the last host CPU metric value.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<MetricEntity>: Last host CPU metric.
   */
  async getHostLastCpu(): Promise<MetricEntity> {
    return this.client.get<MetricEntity>(`${this.prefix}/host/cpu/last`)
  }

  /**
   * Gets the last host RAM metric value.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<MetricEntity>: Last host RAM metric.
   */
  async getHostLastRam(): Promise<MetricEntity> {
    return this.client.get<MetricEntity>(`${this.prefix}/host/ram/last`)
  }

  /**
   * Gets all host CPU metric values.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<MetricEntity[]>: List of host CPU metrics.
   */
  async getHostAllCpu(): Promise<MetricEntity[]> {
    return this.client.get<MetricEntity[]>(`${this.prefix}/host/cpu/all`)
  }

  /**
   * Gets all host RAM metric values.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<MetricEntity[]>: List of host RAM metrics.
   */
  async getHostAllRam(): Promise<MetricEntity[]> {
    return this.client.get<MetricEntity[]>(`${this.prefix}/host/ram/all`)
  }

  /**
   * Gets the last CPU metric value for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<MetricEntity>: Last server CPU metric.
   */
  async getServerLastCpu(serverId: number): Promise<MetricEntity> {
    return this.client.get<MetricEntity>(`${this.prefix}/servers/${serverId}/cpu/last`)
  }

  /**
   * Gets the last RAM metric value for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<MetricEntity>: Last server RAM metric.
   */
  async getServerLastRam(serverId: number): Promise<MetricEntity> {
    return this.client.get<MetricEntity>(`${this.prefix}/servers/${serverId}/ram/last`)
  }

  /**
   * Gets all CPU metric values for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<MetricEntity[]>: List of server CPU metrics.
   */
  async getServerAllCpu(serverId: number): Promise<MetricEntity[]> {
    return this.client.get<MetricEntity[]>(`${this.prefix}/servers/${serverId}/cpu/all`)
  }

  /**
   * Gets all RAM metric values for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<MetricEntity[]>: List of server RAM metrics.
   */
  async getServerAllRam(serverId: number): Promise<MetricEntity[]> {
    return this.client.get<MetricEntity[]>(`${this.prefix}/servers/${serverId}/ram/all`)
  }
}