/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IWsClient, IWsServersApiService } from "@/contracts"
import { ServersEventsEnum } from "@/types"

/**
 * WebSocket service for servers events.
 */
export class WsServersApiService implements IWsServersApiService {
  private readonly client: IWsClient

  constructor(client: IWsClient) {
    this.client = client
  }

  /**
   * Subscribes to servers states and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming server status.
   *
   * Returns:
   * - void.
   */
  subscribeStates(handler: (status: any) => void): void {
    this.client.listen(ServersEventsEnum.SERVER_STATE, handler)
    this.client.subscribe(ServersEventsEnum.SUBSCRIBE_STATES)
  }

  /**
   * Unsubscribes from servers states and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeStates(handler: (status: any) => void): void {
    this.client.unlisten(ServersEventsEnum.SERVER_STATE, handler)
    this.client.unsubscribe(ServersEventsEnum.UNSUBSCRIBE_STATES)
  }
}