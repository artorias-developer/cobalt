/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Represents an auth login request.
 */
export interface AuthLoginRequest {
  login: string
  password: string
}

/**
 * Represents a change credentials request.
 */
export interface AuthChangeCredentialsRequest {
  login?: string
  old_password?: string
  new_password?: string
}