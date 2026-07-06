/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpRolesApiService } from "@/services"
import type { IHttpClient, IHttpRolesApiService } from "@/contracts"

/**
 * Creates a new instance of HttpRolesApiService.
 *
 * Parameters:
 * - client: IHttpClient instance to use for API requests.
 *
 * Returns:
 * - IHttpRolesApiService: A new HttpRolesApiService instance.
 */
export function createHttpRolesApiService(client: IHttpClient): IHttpRolesApiService {
  return new HttpRolesApiService(client)
}