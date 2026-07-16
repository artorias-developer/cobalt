/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { HttpFilesApiService } from "@/services"
import type { IHttpClient, IHttpFilesApiService } from "@/contracts"

/**
 * Creates a new instance of HttpFilesApiService.
 *
 * Parameters:
 * - client: IHttpClient instance to use for API requests.
 *
 * Returns:
 * - IHttpFilesApiService: A new HttpFilesApiService instance.
 */
export function createHttpFilesApiService(client: IHttpClient): IHttpFilesApiService {
  return new HttpFilesApiService(client)
}