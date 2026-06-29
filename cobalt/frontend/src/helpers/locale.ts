/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { ILocaleHelper } from "@/contracts"

/**
 * LocaleHelper provides utility methods for locale-specific formatting.
 * Uses Intl.DateTimeFormat for formatting dates and times.
 * Timezone can be updated at runtime via setTimezone.
 */
export class LocaleHelper implements ILocaleHelper {
  private timezone: string
  private timeFormatter: Intl.DateTimeFormat
  private timeWithSecondsFormatter: Intl.DateTimeFormat
  private dateTimeFormatter: Intl.DateTimeFormat

  constructor() {
    this.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
    this.timeFormatter = this.createTimeFormatter(this.timezone)
    this.timeWithSecondsFormatter = this.createTimeWithSecondsFormatter(this.timezone)
    this.dateTimeFormatter = this.createDateTimeFormatter(this.timezone)
  }

  /**
   * Converts a UTC±N offset string to a valid IANA timezone name.
   * Intl.DateTimeFormat requires IANA names - Etc/GMT uses inverted sign convention.
   *
   * Parameters:
   * - timezone: Timezone string, either UTC±N or a valid IANA name.
   *
   * Returns:
   * - string: Valid IANA timezone string.
   */
  private toIANA(timezone: string): string {
    const match = timezone.match(/^UTC([+-])(\d+)$/)

    if (!match) return timezone

    const sign = match[1] as string
    const offset = parseInt(match[2] as string, 10)

    if (offset === 0) return "Etc/GMT"

    const etcSign = sign === "+" ? "-" : "+"

    return `Etc/GMT${etcSign}${offset}`
  }

  /**
   * Updates the timezone and rebuilds the formatters.
   *
   * Parameters:
   * - timezone: IANA timezone string or UTC±N offset string.
   *
   * Returns:
   * - void.
   */
  setTimezone(timezone: string): void {
    this.timezone = this.toIANA(timezone)
    this.timeFormatter = this.createTimeFormatter(this.timezone)
    this.timeWithSecondsFormatter = this.createTimeWithSecondsFormatter(this.timezone)
    this.dateTimeFormatter = this.createDateTimeFormatter(this.timezone)
  }

  /**
   * Creates a time formatter for the given timezone.
   *
   * Parameters:
   * - timezone: IANA timezone string.
   *
   * Returns:
   * - Intl.DateTimeFormat: Time formatter instance.
   */
  private createTimeFormatter(timezone: string): Intl.DateTimeFormat {
    return new Intl.DateTimeFormat("ru", {
      hour: "2-digit",
      minute: "2-digit",
      timeZone: timezone
    })
  }

  /**
   * Creates a time formatter with seconds for the given timezone.
   *
   * Parameters:
   * - timezone: IANA timezone string.
   *
   * Returns:
   * - Intl.DateTimeFormat: Time formatter instance with seconds.
   */
  private createTimeWithSecondsFormatter(timezone: string): Intl.DateTimeFormat {
    return new Intl.DateTimeFormat("ru", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      timeZone: timezone
    })
  }

  /**
   * Creates a date and time formatter for the given timezone.
   *
   * Parameters:
   * - timezone: IANA timezone string.
   *
   * Returns:
   * - Intl.DateTimeFormat: Date and time formatter instance.
   */
  private createDateTimeFormatter(timezone: string): Intl.DateTimeFormat {
    return new Intl.DateTimeFormat("ru", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      timeZone: timezone
    })
  }

  /**
   * Formats a date string into a localized "HH:mm" time string.
   *
   * Parameters:
   * - dateString: An ISO date string or any string parseable by `Date`.
   *
   * Returns:
   * - string: Formatted time in "HH:mm" format according to the locale and timezone.
   */
  formatTime(dateString: string): string {
    return this.timeFormatter.format(new Date(dateString))
  }

  /**
   * Formats a date string into a localized "HH:mm:ss" time string.
   *
   * Parameters:
   * - dateString: An ISO date string or any string parseable by `Date`.
   *
   * Returns:
   * - string: Formatted time in "HH:mm:ss" format according to the locale and timezone.
   */
  formatTimeWithSeconds(dateString: string): string {
    return this.timeWithSecondsFormatter.format(new Date(dateString))
  }

  /**
   * Formats a date string into a localized full date and time string.
   *
   * Parameters:
   * - dateString: An ISO date string or any string parseable by `Date`.
   *
   * Returns:
   * - string: Formatted date and time in "DD.MM.YYYY, HH:mm" format according to the locale and timezone.
   */
  formatDateTime(dateString: string): string {
    return this.dateTimeFormatter.format(new Date(dateString))
  }
}