/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpMetricsApiService } from "@/services"
import type { IHttpClient, IHttpMetricsApiService } from "@/contracts"

/**
 * Creates a new instance of HttpMetricsApiService.
 *
 * Parameters:
 * - client: IHttpClient instance to use for API requests.
 *
 * Returns:
 * - IHttpMetricsApiService: A new HttpMetricsApiService instance.
 */
export function createHttpMetricsApiService(client: IHttpClient): IHttpMetricsApiService {
  return new HttpMetricsApiService(client)
}