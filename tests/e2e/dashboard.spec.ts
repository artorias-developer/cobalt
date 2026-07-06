/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"

test.describe("Dashboard page", () => {
  test("Should return 200 on disk metrics reload", async ({ page }) => {
    await page.goto('/', { waitUntil: "domcontentloaded" })

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("disk") && resp.request().method() === "GET"
      ),
      page.locator('.block.disk button[name="reload"]').click(),
    ])

    expect(response.status()).toBe(200)
  })
})