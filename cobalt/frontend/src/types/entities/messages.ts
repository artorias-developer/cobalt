/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Represents a WebSocket message received from the server.
 */
export interface WsMessageEntity<T> {
  type: "message"
  event: string
  data: T
}

/**
 * Represents a WebSocket message bound to a specific server.
 */
export interface WsServerMessageEntity<T> extends WsMessageEntity<T> {
  server_id: number
}
