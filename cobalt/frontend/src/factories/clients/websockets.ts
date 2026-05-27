/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { WebSocketClient } from "@/clients"
import type { IWsClient } from "@/contracts"

/**
 * Creates a new instance of WebSocketClient.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - IWebSocketClient: A new WebSocketClient instance.
 */
export function createWebSocketClient(): IWsClient {
  return new WebSocketClient()
}