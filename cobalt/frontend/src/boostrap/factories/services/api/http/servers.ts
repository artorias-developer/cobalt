/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpServersApiService } from "@/services"
import type { IHttpClient, IHttpServersApiService } from "@/contracts"

/**
 * Creates a new instance of HttpServersApiService.
 *
 * Parameters:
 * - client: IHttpClient instance to use for API requests.
 *
 * Returns:
 * - IHttpServersApiService: A new HttpServersApiService instance.
 */
export function createHttpServersApiService(client: IHttpClient): IHttpServersApiService {
  return new HttpServersApiService(client)
}