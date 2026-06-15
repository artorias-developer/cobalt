/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { WsServersApiService } from "@/services"
import type { IWsClient, IWsServersApiService } from "@/contracts"

/**
 * Creates a new instance of WsServersApiService.
 *
 * Parameters:
 * - client: IWsClient instance to use for API requests.
 *
 * Returns:
 * - IWsServersApiService: A new WsServersApiService instance.
 */
export function createWsServersApiService(client: IWsClient): IWsServersApiService {
  return new WsServersApiService(client)
}