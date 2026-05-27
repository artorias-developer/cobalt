/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IDocumentHelper } from "@/contracts"

/**
 * DocumentHelper provides utility methods for working with DOM document.
 * Uses native DOM APIs to access CSS variables and document properties.
 */
export class DocumentHelper implements IDocumentHelper {
  /**
   * Retrieves the value of a CSS variable from the root (`:root`) element.
   *
   * Parameters:
   * - key: The name of the CSS variable to retrieve, including the `--` prefix.
   *
   * Returns:
   * - string: The trimmed value of the CSS variable.
   */
  getRootStyle(key: string): string {
    return getComputedStyle(document.documentElement)
      .getPropertyValue(key)
      .trim()
  }
}