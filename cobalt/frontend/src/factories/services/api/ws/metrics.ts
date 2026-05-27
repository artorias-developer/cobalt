/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { WsMetricsApiService } from "@/services"
import type { IWsClient, IWsMetricsApiService } from "@/contracts"

/**
 * Creates a new instance of WsMetricsApiService.
 *
 * Parameters:
 * - client: IWsClient instance to use for API requests.
 *
 * Returns:
 * - IWsMetricsApiService: A new WsMetricsApiService instance.
 */
export function createWsMetricsApiService(client: IWsClient): IWsMetricsApiService {
  return new WsMetricsApiService(client)
}