/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Interface for metrics WebSocket service operations.
 * Defines contract for managing live metrics subscriptions.
 * Implementation-agnostic - not tied to any specific WS client.
 */
export interface IWsMetricsApiService {
  /**
   * Subscribes to host CPU live metrics and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming metric updates.
   *
   * Returns:
   * - void.
   */
  subscribeHostCpu(handler: (metric: any) => void): void

  /**
   * Unsubscribes from host CPU live metrics and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeHostCpu(handler: (metric: any) => void): void

  /**
   * Subscribes to host RAM live metrics and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming metric updates.
   *
   * Returns:
   * - void.
   */
  subscribeHostRam(handler: (metric: any) => void): void

  /**
   * Unsubscribes from host RAM live metrics and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeHostRam(handler: (metric: any) => void): void

  /**
   * Subscribes to server CPU live metrics and registers a handler.
   *
   * Parameters:
   * - serverId: Server ID.
   * - handler: Callback function for incoming metric updates.
   *
   * Returns:
   * - void.
   */
  subscribeServerCpu(serverId: number, handler: (metric: any) => void): void

  /**
   * Unsubscribes from server CPU live metrics and removes the handler.
   *
   * Parameters:
   * - serverId: Server ID.
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeServerCpu(serverId: number, handler: (metric: any) => void): void

  /**
   * Subscribes to server RAM live metrics and registers a handler.
   *
   * Parameters:
   * - serverId: Server ID.
   * - handler: Callback function for incoming metric updates.
   *
   * Returns:
   * - void.
   */
  subscribeServerRam(serverId: number, handler: (metric: any) => void): void

  /**
   * Unsubscribes from server RAM live metrics and removes the handler.
   *
   * Parameters:
   * - serverId: Server ID.
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeServerRam(serverId: number, handler: (metric: any) => void): void
}