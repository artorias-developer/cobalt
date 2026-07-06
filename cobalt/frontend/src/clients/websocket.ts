/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IWsClient, MessageHandler } from "@/contracts"

/**
 * WebSocket client implementation using native WebSocket API.
 * Provides:
 * - Automatic reconnection
 * - Event-based subscriptions
 * - Message queuing while disconnected
 * - Multiple event handlers per event
 */
export class WebSocketClient implements IWsClient {
  private ws: WebSocket | null = null
  private handlers: Map<string, Set<MessageHandler>> = new Map()
  private reconnectTimeout: number = 3000
  private reconnectTimer: any = null
  private pendingMessages: Array<{ event: string, data?: any }> = []
  private url: string = ""
  private subscriptions: Map<string, any> = new Map()

  /**
   * Connects to a WebSocket server at the given URL.
   *
   * Parameters:
   * - url: WebSocket server URL to connect to.
   *
   * Returns:
   * - void.
   */
  connect(url: string): void {
    this.url = url
    this.ws = new WebSocket(url)

    this.ws.onopen = () => {
      console.log("WebSocket connected")

      this.subscriptions.forEach((data, event) => {
        this.send(event, data)
      })

      while (this.pendingMessages.length > 0) {
        const msg = this.pendingMessages.shift()!
        this.send(msg.event, msg.data)
      }
    }

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data)

      if (message.type === "message") {
        const handlers = this.handlers.get(message.event)

        if (handlers) {
          handlers.forEach(handler => handler(message))
        }
      } else if (message.type === "error") {
        console.error(`WebSocket error [${message.code}]: ${message.data}`)
      }
    }

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error)
    }

    this.ws.onclose = (event) => {
      console.log(`WebSocket closed [${event.code}]: ${event.reason}`)
      this.reconnectTimer = setTimeout(() => this.connect(this.url), this.reconnectTimeout)
    }
  }

  /**
   * Returns whether the WebSocket is currently connected.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - boolean: `true` if connected, `false` otherwise.
   */
  isConnected(): boolean {
    return (
      this.ws?.readyState === WebSocket.OPEN ||
      this.ws?.readyState === WebSocket.CONNECTING ||
      this.reconnectTimer !== null
    )
  }

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
  send(event: string, data?: any): void {
    const message = {
      type: "action",
      event: event,
      data: data || {}
    }

    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    } else {
      this.pendingMessages.push({event, data})
    }
  }

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
  subscribe(event: string, data?: any): void {
    this.subscriptions.set(event, data || {})
    this.send(event, data)
  }

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
  unsubscribe(event: string, data?: any): void {
    this.subscriptions.delete(event)
    this.send(event, data)
  }

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
  listen(event: string, handler: MessageHandler): void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set())
    }
    this.handlers.get(event)!.add(handler)
  }

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
  unlisten(event: string, handler: MessageHandler): void {
    const handlers = this.handlers.get(event)
    if (handlers) {
      handlers.delete(handler)
    }
  }

  /**
   * Reconnects to the WebSocket server.
   * Clears any pending reconnect timer, closes the existing connection,
   * and immediately initiates a new connection to the same URL.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void.
   */
  reconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    this.ws?.close()
    this.connect(this.url)
  }

  /**
   * Disconnects from the WebSocket server.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void.
   */
  disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    this.ws?.close()
  }
}