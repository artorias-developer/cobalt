/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Represents a settings update request.
 */
export interface SettingsUpdateRequest {
  language?: string
  theme?: string
  timezone?: string
}