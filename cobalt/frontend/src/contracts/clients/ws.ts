/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

type MessageHandler = (data: any) => void

/**
 * Interface for WebSocket client operations.
 * Defines contract for real-time bidirectional communication.
 * Implementation-agnostic - not tied to any specific WebSocket library.
 */
export interface IWsClient {
  /**
   * Connects to a WebSocket server at the given URL.
   *
   * Parameters:
   * - url: WebSocket server URL to connect to.
   *
   * Returns:
   * - void.
   */
  connect(url: string): void

  /**
   * Returns whether the WebSocket is currently connected.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - boolean: `true` if connected, `false` otherwise.
   */
  isConnected(): boolean

  /**
   * Sends an action message to the WebSocket server.
   *
   * Parameters:
   * - event: The name of the event to send.
   * - data?: Optional payload for the event.
   *
   * Returns:
   * - void.
   */
  send(event: string, data?: any): void

  /**
   * Subscribes to a server-side event and sends initial data if provided.
   *
   * Parameters:
   * - event: The name of the event to subscribe to.
   * - data?: Optional payload for the subscription.
   *
   * Returns:
   * - void.
   */
  subscribe(event: string, data?: any): void

  /**
   * Unsubscribes from a server-side event.
   *
   * Parameters:
   * - event: The name of the event to unsubscribe from.
   * - data?: Optional payload for the unsubscription message.
   *
   * Returns:
   * - void.
   */
  unsubscribe(event: string, data?: any): void

  /**
   * Registers a handler function for a specific event.
   *
   * Parameters:
   * - event: The event name to listen for.
   * - handler: A callback to execute when the event is received.
   *
   * Returns:
   * - void.
   */
  listen(event: string, handler: MessageHandler): void

  /**
   * Removes a previously registered handler for a specific event.
   *
   * Parameters:
   * - event: The event name.
   * - handler: The handler to remove.
   *
   * Returns:
   * - void.
   */
  unlisten(event: string, handler: MessageHandler): void

  /**
   * Disconnects from the WebSocket server.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void.
   */
  disconnect(): void
}

export type { MessageHandler }