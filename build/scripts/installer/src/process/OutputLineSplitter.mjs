/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Splits a stream of output chunks into complete lines.
 */
export class OutputLineSplitter {
  /**
   * Creates an empty splitter.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - OutputLineSplitter: A new splitter instance.
   */
  constructor() {
    this.pendingText = "";
  }

  /**
   * Adds a chunk and returns every line that is now complete.
   *
   * Parameters:
   * - chunk (Buffer|string): Raw output chunk.
   *
   * Returns:
   * - string[]: Completed lines (without line terminators).
   */
  push(chunk) {
    this.pendingText += chunk.toString();
    const lines = this.pendingText.split(/\r\n|\n|\r/);
    this.pendingText = lines.pop();
    return lines;
  }

  /**
   * Returns and clears the trailing incomplete line.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - string: The remaining text (may be empty).
   */
  flush() {
    const remainingText = this.pendingText;
    this.pendingText = "";
    return remainingText;
  }
}