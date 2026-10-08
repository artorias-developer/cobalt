/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Error raised when an external command fails.
 */
export class CommandError extends Error {
  /**
   * Creates a command error.
   *
   * Parameters:
   * - message (string): Human-readable description.
   * - exitCode (number): Exit code of the failed command.
   * - outputTail (string[]): Last lines of command output.
   *
   * Returns:
   * - CommandError: A new error instance.
   */
  constructor(message, exitCode = 1, outputTail = []) {
    super(message);
    this.exitCode = exitCode;
    this.outputTail = outputTail;
  }
}