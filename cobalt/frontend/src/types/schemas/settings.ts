/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
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