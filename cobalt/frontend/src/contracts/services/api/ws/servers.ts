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
export interface IWsServersApiService {
  /**
   * Subscribes to servers states and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming server status.
   *
   * Returns:
   * - void.
   */
  subscribeStates(handler: (status: any) => void): void

  /**
   * Unsubscribes from servers states and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeStates(handler: (status: any) => void): void
}