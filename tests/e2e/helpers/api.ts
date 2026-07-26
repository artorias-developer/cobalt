/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { Page, Response } from "@playwright/test"
import { expect } from "@playwright/test"

/**
 * Navigates to a page with retries on transient network errors.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - url: URL to navigate to.
 * - retries: Number of retry attempts on transient failures.
 *
 * Returns:
 * - Promise<void>.
 */
export async function gotoWithRetry(
  page: Page,
  url: string,
  retries = 3,
): Promise<void> {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      await page.goto(url, { waitUntil: "domcontentloaded" })
      return
    } catch (error) {
      const isTransient =
        error instanceof Error &&
        /ERR_NETWORK_CHANGED|ERR_CONNECTION_REFUSED|ERR_CONNECTION_RESET|ERR_EMPTY_RESPONSE/.test(
          error.message,
        )

      if (!isTransient || attempt === retries) {
        throw error
      }

      await page.waitForTimeout(500 * attempt)
    }
  }
}

/**
 * Waits for a specific API response matching a URL pattern and HTTP method.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - urlMatch: Pattern to match against the response URL.
 * - method: HTTP method to match (e.g. "POST", "GET").
 *
 * Returns:
 * - Promise<Response>: the matched response.
 */
export function waitForApi(
  page: Page,
  urlMatch: RegExp,
  method: string,
): Promise<Response> {
  page.on("requestfailed", (req) => {
    console.log(
      "[FAILED]",
      req.method(),
      req.url(),
      req.failure()?.errorText,
    )
  })

  return page.waitForResponse(
    (resp) => urlMatch.test(resp.url()) && resp.request().method() === method,
    { timeout: 15_000 },
  )
}

/**
 * Clicks a locator and waits for the resulting API response.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - locatorSelector: CSS selector for the element to click.
 * - urlMatch: Pattern to match against the response URL.
 * - method: HTTP method to match (e.g. "POST", "GET").
 *
 * Returns:
 * - Promise<Response>: the response triggered by the click.
 */
export async function clickAndWaitForApi(
  page: Page,
  locatorSelector: string,
  urlMatch: RegExp,
  method: string,
): Promise<Response> {
  const locator = page.locator(locatorSelector)
  await locator.waitFor({ state: "visible" })
  await expect(locator).toBeEnabled()

  const responsePromise = waitForApi(page, urlMatch, method)
  await locator.click()
  return responsePromise
}