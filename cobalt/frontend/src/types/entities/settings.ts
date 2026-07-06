/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Represents a settings object.
 */
export interface SettingsEntity {
  id: number
  user_id: number
  language: string
  theme: string
  timezone: string
  created_at: string
  updated_at: string
}