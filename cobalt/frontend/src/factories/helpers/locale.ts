/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { LocaleHelper } from "@/helpers"
import type { ILocaleHelper } from "@/contracts"

/**
 * Creates a new instance of LocaleHelper.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - ILocaleHelper: A new LocaleHelper instance.
 */
export function createLocaleHelper(): ILocaleHelper {
  return new LocaleHelper()
}