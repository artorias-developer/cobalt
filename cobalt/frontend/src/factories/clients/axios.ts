/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpAxiosClient } from "@/clients"
import type { IHttpClient } from "@/contracts"

/**
 * Creates a new instance of HttpAxiosClient.
 *
 * Parameters:
 * - baseURL: Base URL for all API requests (default: empty string).
 *
 * Returns:
 * - IHttpClient: A new HttpAxiosClient instance.
 */
export function createHttpAxiosClient(baseURL?: string): IHttpClient {
  return new HttpAxiosClient(baseURL)
}