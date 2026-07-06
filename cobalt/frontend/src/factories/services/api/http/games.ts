/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpGamesApiService } from "@/services"
import type { IHttpClient, IHttpGamesApiService } from "@/contracts"

/**
 * Creates a new instance of HttpGamesApiService.
 *
 * Parameters:
 * - client: IHttpClient instance to use for API requests.
 *
 * Returns:
 * - IHttpGamesApiService: A new HttpGamesApiService instance.
 */
export function createHttpGamesApiService(client: IHttpClient): IHttpGamesApiService {
  return new HttpGamesApiService(client)
}