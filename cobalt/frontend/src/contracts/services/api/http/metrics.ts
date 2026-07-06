/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { DiskMetricsEntity, MetricEntity } from "@/types"

/**
 * Interface for metrics API service operations.
 * Defines contract for fetching host and server metrics.
 * Implementation-agnostic - not tied to any specific HTTP client.
 */
export interface IHttpMetricsApiService {
  /**
   * Gets host disk usage metrics.
   *
   * Parameters:
   * - refresh: If true, bypasses cache and fetches fresh data (default: false).
   *
   * Returns:
   * - Promise<DiskMetricsEntity>: Host disk metrics.
   */
  getHostDisk(refresh?: boolean): Promise<DiskMetricsEntity>

  /**
   * Gets the last host CPU metric value.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<MetricEntity>: Last host CPU metric.
   */
  getHostLastCpu(): Promise<MetricEntity>

  /**
   * Gets the last host RAM metric value.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<MetricEntity>: Last host RAM metric.
   */
  getHostLastRam(): Promise<MetricEntity>

  /**
   * Gets all host CPU metric values.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<MetricEntity[]>: List of host CPU metrics.
   */
  getHostAllCpu(): Promise<MetricEntity[]>

  /**
   * Gets all host RAM metric values.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<MetricEntity[]>: List of host RAM metrics.
   */
  getHostAllRam(): Promise<MetricEntity[]>

  /**
   * Gets the last CPU metric value for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<MetricEntity>: Last server CPU metric.
   */
  getServerLastCpu(serverId: number): Promise<MetricEntity>

  /**
   * Gets the last RAM metric value for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<MetricEntity>: Last server RAM metric.
   */
  getServerLastRam(serverId: number): Promise<MetricEntity>

  /**
   * Gets all CPU metric values for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<MetricEntity[]>: List of server CPU metrics.
   */
  getServerAllCpu(serverId: number): Promise<MetricEntity[]>

  /**
   * Gets all RAM metric values for a specific server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<MetricEntity[]>: List of server RAM metrics.
   */
  getServerAllRam(serverId: number): Promise<MetricEntity[]>
}