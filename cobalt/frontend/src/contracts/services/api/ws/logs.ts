/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Interface for logs WebSocket service operations.
 * Defines contract for managing live log subscriptions.
 * Implementation-agnostic - not tied to any specific WS client.
 */
export interface IWsLogsApiService {
  /**
   * Subscribes to host live logs and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming log messages.
   *
   * Returns:
   * - void.
   */
  subscribeHost(handler: (log: any) => void): void

  /**
   * Unsubscribes from host live logs and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeHost(handler: (log: any) => void): void

  /**
   * Subscribes to server live logs and registers a handler.
   *
   * Parameters:
   * - serverId: Server ID.
   * - handler: Callback function for incoming log messages.
   *
   * Returns:
   * - void.
   */
  subscribeServer(serverId: number, handler: (log: any) => void): void

  /**
   * Unsubscribes from server live logs and removes the handler.
   *
   * Parameters:
   * - serverId: Server ID.
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeServer(serverId: number, handler: (log: any) => void): void
}