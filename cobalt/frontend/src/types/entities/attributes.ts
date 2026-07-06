/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Represents a server attribute.
 */
export interface AttributeEntity {
  id: number
  server_id: number
  key: string
  value: string
  created_at: string
  updated_at: string
}