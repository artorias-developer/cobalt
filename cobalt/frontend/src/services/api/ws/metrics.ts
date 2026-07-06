/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IWsClient, IWsMetricsApiService } from "@/contracts"
import { MetricsEventEnum } from "@/types"

/**
 * WebSocket service for metrics events.
 */
export class WsMetricsApiService implements IWsMetricsApiService {
  private readonly client: IWsClient

  constructor(client: IWsClient) {
    this.client = client
  }

  /**
   * Subscribes to host CPU live metrics and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming metric updates.
   *
   * Returns:
   * - void.
   */
  subscribeHostCpu(handler: (message: any) => void): void {
    this.client.listen(MetricsEventEnum.HOST_CPU_METRIC, handler)
    this.client.subscribe(MetricsEventEnum.SUBSCRIBE_HOST_CPU)
  }

  /**
   * Unsubscribes from host CPU live metrics and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeHostCpu(handler: (message: any) => void): void {
    this.client.unlisten(MetricsEventEnum.HOST_CPU_METRIC, handler)
    this.client.unsubscribe(MetricsEventEnum.UNSUBSCRIBE_HOST_CPU)
  }

  /**
   * Subscribes to host RAM live metrics and registers a handler.
   *
   * Parameters:
   * - handler: Callback function for incoming metric updates.
   *
   * Returns:
   * - void.
   */
  subscribeHostRam(handler: (message: any) => void): void {
    this.client.listen(MetricsEventEnum.HOST_RAM_METRIC, handler)
    this.client.subscribe(MetricsEventEnum.SUBSCRIBE_HOST_RAM)
  }

  /**
   * Unsubscribes from host RAM live metrics and removes the handler.
   *
   * Parameters:
   * - handler: Callback function to remove.
   *
   * Returns:
   * - void.
   */
  unsubscribeHostRam(handler: (message: any) => void): void {
    this.client.unlisten(MetricsEventEnum.HOST_RAM_METRIC, handler)
    this.client.unsubscribe(MetricsEventEnum.UNSUBSCRIBE_HOST_RAM)
  }

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
  subscribeServerCpu(serverId: number, handler: (message: any) => void): void {
    this.client.listen(MetricsEventEnum.SERVER_CPU_METRIC, handler)
    this.client.subscribe(MetricsEventEnum.SUBSCRIBE_SERVER_CPU, {
      server_id: serverId
    })
  }

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
  unsubscribeServerCpu(serverId: number, handler: (message: any) => void): void {
    this.client.unlisten(MetricsEventEnum.SERVER_CPU_METRIC, handler)
    this.client.unsubscribe(MetricsEventEnum.UNSUBSCRIBE_SERVER_CPU, {
      server_id: serverId
    })
  }

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
  subscribeServerRam(serverId: number, handler: (message: any) => void): void {
    this.client.listen(MetricsEventEnum.SERVER_RAM_METRIC, handler)
    this.client.subscribe(MetricsEventEnum.SUBSCRIBE_SERVER_RAM, {
      server_id: serverId
    })
  }

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
  unsubscribeServerRam(serverId: number, handler: (message: any) => void): void {
    this.client.unlisten(MetricsEventEnum.SERVER_RAM_METRIC, handler)
    this.client.unsubscribe(MetricsEventEnum.UNSUBSCRIBE_SERVER_RAM, {
      server_id: serverId
    })
  }
}