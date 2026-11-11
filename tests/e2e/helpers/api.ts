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
  const base = process.env.COBALT_BASE ?? ""
  const path = url.startsWith("/") ? url.slice(1) : url
  const fullPath = [base, path].filter(Boolean).join("/")

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      await page.goto(fullPath, { waitUntil: "domcontentloaded" })
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

/**
 * Builds a minimal ZIP archive (stored, no compression) in memory.
 *
 * Parameters:
 * - entries: Map of file names to their text content.
 *
 * Returns:
 * - Buffer: ZIP archive bytes.
 */
export function createZip(entries: Record<string, string>): Buffer {
  const crcTable = Array.from({ length: 256 }, (_, n) => {
    let c = n
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1
    return c >>> 0
  })
  const crc32 = (data: Buffer): number => {
    let crc = 0xffffffff
    for (const byte of data) crc = crcTable[(crc ^ byte) & 0xff]! ^ (crc >>> 8)
    return (crc ^ 0xffffffff) >>> 0
  }

  const locals: Buffer[] = []
  const centrals: Buffer[] = []
  let offset = 0

  for (const [name, content] of Object.entries(entries)) {
    const nameBuffer = Buffer.from(name)
    const data = Buffer.from(content)
    const crc = crc32(data)

    const local = Buffer.alloc(30)
    local.writeUInt32LE(0x04034b50, 0)
    local.writeUInt16LE(20, 4)
    local.writeUInt32LE(crc, 14)
    local.writeUInt32LE(data.length, 18)
    local.writeUInt32LE(data.length, 22)
    local.writeUInt16LE(nameBuffer.length, 26)
    locals.push(local, nameBuffer, data)

    const central = Buffer.alloc(46)
    central.writeUInt32LE(0x02014b50, 0)
    central.writeUInt16LE(20, 4)
    central.writeUInt16LE(20, 6)
    central.writeUInt32LE(crc, 16)
    central.writeUInt32LE(data.length, 20)
    central.writeUInt32LE(data.length, 24)
    central.writeUInt16LE(nameBuffer.length, 28)
    central.writeUInt32LE(offset, 42)
    centrals.push(central, nameBuffer)

    offset += local.length + nameBuffer.length + data.length
  }

  const centralSize = centrals.reduce((size, part) => size + part.length, 0)
  const count = Object.keys(entries).length

  const end = Buffer.alloc(22)
  end.writeUInt32LE(0x06054b50, 0)
  end.writeUInt16LE(count, 8)
  end.writeUInt16LE(count, 10)
  end.writeUInt32LE(centralSize, 12)
  end.writeUInt32LE(offset, 16)

  return Buffer.concat([...locals, ...centrals, end])
}
