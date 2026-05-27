/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { DocumentHelper } from "@/helpers"
import type { IDocumentHelper } from "@/contracts"

/**
 * Creates a new instance of DocumentHelper.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - IDocumentHelper: A new DocumentHelper instance.
 */
export function createDocumentHelper(): IDocumentHelper {
  return new DocumentHelper()
}