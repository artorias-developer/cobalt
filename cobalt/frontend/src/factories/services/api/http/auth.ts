/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpAuthApiService } from "@/services"
import type { IHttpClient, IHttpAuthApiService } from "@/contracts"

/**
 * Creates a new instance of HttpAuthApiService.
 *
 * Parameters:
 * - client: IHttpClient instance to use for API requests.
 *
 * Returns:
 * - IHttpAuthApiService: A new HttpAuthApiService instance.
 */
export function createHttpAuthApiService(client: IHttpClient): IHttpAuthApiService {
  return new HttpAuthApiService(client)
}