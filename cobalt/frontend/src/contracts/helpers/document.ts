/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Interface for DOM document utility operations.
 * Defines contract for working with CSS variables and document properties.
 * Implementation-agnostic - not tied to any specific DOM API.
 */
export interface IDocumentHelper {
  /**
   * Retrieves the value of a CSS variable from the root (`:root`) element.
   *
   * Parameters:
   * - key: The name of the CSS variable to retrieve, including the `--` prefix.
   *
   * Returns:
   * - string: The trimmed value of the CSS variable.
   */
  getRootStyle(key: string): string
}