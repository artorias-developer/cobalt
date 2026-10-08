/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import process from "node:process";

import { TerminalStyle } from "../ui/TerminalStyle.mjs";

/**
 * Draws a single-line progress bar with a spinner for a ProgressTracker.
 */
export class ProgressRenderer {
  static BAR_WIDTH = 30;
  static SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
  static REFRESH_INTERVAL_MILLISECONDS = 80;

  /**
   * Creates a renderer.
   *
   * Parameters:
   * - tracker (ProgressTracker): Source of percentage and label.
   *
   * Returns:
   * - ProgressRenderer: A new renderer instance.
   */
  constructor(tracker) {
    this.tracker = tracker;
    this.timer = null;
    this.frameIndex = 0;
  }

  /**
   * Starts the animated progress line.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void: Nothing.
   */
  start() {
    TerminalStyle.hideCursor();
    this.timer = setInterval(() => this.#draw(), ProgressRenderer.REFRESH_INTERVAL_MILLISECONDS);
    this.#draw();
  }

  /**
   * Stops the animation, clears the line and restores the cursor.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void: Nothing.
   */
  stop() {
    clearInterval(this.timer);
    TerminalStyle.clearLine();
    TerminalStyle.showCursor();
  }

  /**
   * Builds the full progress line for the current state.
   *
   * Parameters:
   * - icon (string): Status icon shown before the bar.
   *
   * Returns:
   * - string: The formatted line.
   */
  formatLine(icon) {
    const percentText = String(Math.floor(this.tracker.percent + 1e-9)).padStart(3);
    const label = this.#fitLabel(this.tracker.label);
    return `${TerminalStyle.gutter}${icon}  ${this.#buildBar(this.tracker.percent)} ${percentText}%  ${label}`;
  }

  /**
   * Draws one animation frame.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void: Nothing.
   */
  #draw() {
    const frames = ProgressRenderer.SPINNER_FRAMES;
    const icon = TerminalStyle.cyan(frames[this.frameIndex++ % frames.length]);
    TerminalStyle.clearLine();
    process.stdout.write(this.formatLine(icon));
  }

  /**
   * Builds the bar graphic.
   *
   * Parameters:
   * - percent (number): Completion percentage.
   *
   * Returns:
   * - string: The styled bar.
   */
  #buildBar(percent) {
    const filledCount = Math.round((ProgressRenderer.BAR_WIDTH * percent) / 100);
    const emptyCount = ProgressRenderer.BAR_WIDTH - filledCount;
    return TerminalStyle.cyan("█".repeat(filledCount)) + TerminalStyle.gray("░".repeat(emptyCount));
  }

  /**
   * Truncates a label so the line fits the terminal width.
   *
   * Parameters:
   * - label (string): Label to fit.
   *
   * Returns:
   * - string: The original or truncated label.
   */
  #fitLabel(label) {
    const columnCount = process.stdout.columns || 80;
    const availableWidth = Math.max(10, columnCount - (3 + 3 + ProgressRenderer.BAR_WIDTH + 7));
    return label.length > availableWidth ? `${label.slice(0, availableWidth - 1)}…` : label;
  }
}