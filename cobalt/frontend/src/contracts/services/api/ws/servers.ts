/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Interface for logs WebSocket service operations.
 * Defines contract for managing live log subscriptions.
 * Implementation-agnostic - not tied to any specific WS client.
 */
export interface IWsServersApiService {
  /**
   * Subscribes to servers statuses and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming server status.
   *
   * Returns:
   * - void.
   */
  subscribeStatuses(handler: (status: any) => void): void

  /**
   * Unsubscribes from servers statuses and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeStatuses(handler: (status: any) => void): void
}