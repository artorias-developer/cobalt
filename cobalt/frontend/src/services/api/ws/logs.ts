/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IWsClient, IWsLogsApiService } from "@/contracts"
import { LogsEventEnum } from "@/types"

/**
 * WebSocket service for logs events.
 */
export class WsLogsApiService implements IWsLogsApiService {
  private readonly client: IWsClient

  constructor(client: IWsClient) {
    this.client = client
  }

  /**
   * Subscribes to host live logs and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming log messages.
   *
   * Returns:
   * - void.
   */
  subscribeHost(handler: (message: any) => void): void {
    this.client.listen(LogsEventEnum.HOST_LOG, handler)
    this.client.subscribe(LogsEventEnum.SUBSCRIBE_HOST)
  }

  /**
   * Unsubscribes from host live logs and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeHost(handler: (message: any) => void): void {
    this.client.unlisten(LogsEventEnum.HOST_LOG, handler)
    this.client.unsubscribe(LogsEventEnum.UNSUBSCRIBE_HOST)
  }

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
  subscribeServer(serverId: number, handler: (message: any) => void): void {
    this.client.listen(LogsEventEnum.SERVER_LOG, handler)
    this.client.subscribe(LogsEventEnum.SUBSCRIBE_SERVER, {
      server_id: serverId
    })
  }

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
  unsubscribeServer(serverId: number, handler: (message: any) => void): void {
    this.client.unlisten(LogsEventEnum.SERVER_LOG, handler)
    this.client.unsubscribe(LogsEventEnum.UNSUBSCRIBE_SERVER, {
      server_id: serverId
    })
  }
}