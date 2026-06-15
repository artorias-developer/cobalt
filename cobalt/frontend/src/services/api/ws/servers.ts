/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
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
   * Subscribes to servers statuses and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming server status.
   *
   * Returns:
   * - void.
   */
  subscribeStatuses(handler: (status: any) => void): void {
    this.client.listen(ServersEventsEnum.SERVER_STATUS, handler)
    this.client.subscribe(ServersEventsEnum.SUBSCRIBE_STATUSES)
  }

  /**
   * Unsubscribes from servers statuses and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeStatuses(handler: (status: any) => void): void {
    this.client.unlisten(ServersEventsEnum.SERVER_STATUS, handler)
    this.client.unsubscribe(ServersEventsEnum.UNSUBSCRIBE_STATUSES)
  }
}