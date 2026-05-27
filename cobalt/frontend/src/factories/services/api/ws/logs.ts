/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { WsLogsApiService } from "@/services"
import type { IWsClient, IWsLogsApiService } from "@/contracts"

/**
 * Creates a new instance of WsLogsApiService.
 *
 * Parameters:
 * - client: IWsClient instance to use for API requests.
 *
 * Returns:
 * - IWsLogsApiService: A new WsLogsApiService instance.
 */
export function createWsLogsApiService(client: IWsClient): IWsLogsApiService {
  return new WsLogsApiService(client)
}