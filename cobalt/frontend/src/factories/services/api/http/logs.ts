/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpLogsApiService } from "@/services"
import type { IHttpClient, IHttpLogsApiService } from "@/contracts"

/**
 * Creates a new instance of HttpLogsApiService.
 *
 * Parameters:
 * - client: IHttpClient instance to use for API requests.
 *
 * Returns:
 * - IHttpLogsApiService: A new HttpLogsApiService instance.
 */
export function createHttpLogsApiService(client: IHttpClient): IHttpLogsApiService {
  return new HttpLogsApiService(client)
}