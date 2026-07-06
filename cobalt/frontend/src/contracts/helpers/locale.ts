/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Interface for locale-specific formatting operations.
 * Defines contract for date and time formatting.
 * Implementation-agnostic - not tied to any specific formatting library.
 */
export interface ILocaleHelper {
  /**
   * Updates the timezone and rebuilds the formatters.
   *
   * Parameters:
   * - timezone: IANA timezone string.
   *
   * Returns:
   * - void.
   */
  setTimezone(timezone: string): void

  /**
   * Formats a date string into a localized "HH:mm" time string.
   *
   * Parameters:
   * - dateString: An ISO date string or any string parseable by `Date`.
   *
   * Returns:
   * - string: Formatted time in "HH:mm" format according to the locale.
   */
  formatTime(dateString: string): string

  /**
   * Formats a date string into a localized "HH:mm:ss" time string.
   *
   * Parameters:
   * - dateString: An ISO date string or any string parseable by `Date`.
   *
   * Returns:
   * - string: Formatted time in "HH:mm:ss" format according to the locale.
   */
  formatTimeWithSeconds(dateString: string): string

  /**
   * Formats a date string into a localized full date and time string.
   *
   * Parameters:
   * - dateString: An ISO date string or any string parseable by `Date`.
   *
   * Returns:
   * - string: Formatted date and time in "DD.MM.YYYY, HH:mm" format according to the locale.
   */
  formatDateTime(dateString: string): string
}