/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import process from "node:process";

/**
 * Terminal styling helpers: colors, cursor control and ANSI stripping.
 */
export class TerminalStyle {
  static ESCAPE_SEQUENCE = "\x1b[";

  /**
   * Wraps text in an ANSI color sequence.
   *
   * Parameters:
   * - colorCode (number): ANSI SGR code to apply.
   * - text (string): Text to colorize.
   *
   * Returns:
   * - string: The colorized text.
   */
  static paint(colorCode, text) {
    return `${TerminalStyle.ESCAPE_SEQUENCE}${colorCode}m${text}${TerminalStyle.ESCAPE_SEQUENCE}0m`;
  }

  /**
   * Colors text cyan.
   *
   * Parameters:
   * - text (string): Text to colorize.
   *
   * Returns:
   * - string: The cyan text.
   */
  static cyan(text) {
    return TerminalStyle.paint(36, text);
  }

  /**
   * Colors text green.
   *
   * Parameters:
   * - text (string): Text to colorize.
   *
   * Returns:
   * - string: The green text.
   */
  static green(text) {
    return TerminalStyle.paint(32, text);
  }

  /**
   * Colors text red.
   *
   * Parameters:
   * - text (string): Text to colorize.
   *
   * Returns:
   * - string: The red text.
   */
  static red(text) {
    return TerminalStyle.paint(31, text);
  }

  /**
   * Colors text gray.
   *
   * Parameters:
   * - text (string): Text to colorize.
   *
   * Returns:
   * - string: The gray text.
   */
  static gray(text) {
    return TerminalStyle.paint(90, text);
  }

  /**
   * Dims text.
   *
   * Parameters:
   * - text (string): Text to dim.
   *
   * Returns:
   * - string: The dimmed text.
   */
  static dim(text) {
    return TerminalStyle.paint(2, text);
  }

  /**
   * Left gutter that visually joins custom output with the prompt flow.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - string: The styled gutter prefix.
   */
  static get gutter() {
    return `${TerminalStyle.gray("│")}  `;
  }

  /**
   * Removes ANSI escape sequences from text.
   *
   * Parameters:
   * - text (string): Text that may contain escape sequences.
   *
   * Returns:
   * - string: The plain text.
   */
  static stripAnsi(text) {
    return text.replace(/\x1b\[[0-9;?]*[A-Za-z]/g, "");
  }

  /**
   * Hides the terminal cursor.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void: Nothing.
   */
  static hideCursor() {
    process.stdout.write(`${TerminalStyle.ESCAPE_SEQUENCE}?25l`);
  }

  /**
   * Shows the terminal cursor.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void: Nothing.
   */
  static showCursor() {
    process.stdout.write(`${TerminalStyle.ESCAPE_SEQUENCE}?25h`);
  }

  /**
   * Clears the current terminal line and returns the cursor to its start.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void: Nothing.
   */
  static clearLine() {
    process.stdout.write(`\r${TerminalStyle.ESCAPE_SEQUENCE}2K`);
  }
}