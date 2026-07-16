/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpUsersApiService } from "@/services"
import type { IHttpClient, IHttpUsersApiService } from "@/contracts"

/**
 * Creates a new instance of HttpUsersApiService.
 *
 * Parameters:
 * - client: IHttpClient instance to use for API requests.
 *
 * Returns:
 * - IHttpUsersApiService: A new HttpUsersApiService instance.
 */
export function createHttpUsersApiService(client: IHttpClient): IHttpUsersApiService {
  return new HttpUsersApiService(client)
}