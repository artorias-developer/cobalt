/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpSettingsApiService } from "@/services"
import type { IHttpClient, IHttpSettingsApiService } from "@/contracts"

/**
 * Creates a new instance of HttpSettingsApiService.
 *
 * Parameters:
 * - client: IHttpClient instance to use for API requests.
 *
 * Returns:
 * - IHttpSettingsApiService: A new HttpSettingsApiService instance.
 */
export function createHttpSettingsApiService(client: IHttpClient): IHttpSettingsApiService {
  return new HttpSettingsApiService(client)
}