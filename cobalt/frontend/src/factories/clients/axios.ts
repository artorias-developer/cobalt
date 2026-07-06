/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { Router } from "vue-router"

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
export function createHttpAxiosClient(router: Router, baseURL?: string): IHttpClient {
  return new HttpAxiosClient(router, baseURL)
}