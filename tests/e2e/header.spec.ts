/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"
import { gotoWithRetry } from "./helpers/api.js"

test.describe("Header", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/")
  })

  test("Should open Settings security tab on header item click", async ({ page }) => {
    const link = page.locator('.header a[aria-label="settings-security"]')
    await link.waitFor({ state: "visible" })
    await expect(link).toBeEnabled()
    await link.click()

    await expect(page).toHaveURL("/settings")

    const tab = page.locator('.page .block.settings .tabs .nav button[name="security"].active')
    await tab.waitFor({ state: "visible" })
    await expect(tab).toBeVisible()
  })

  test("Should open Settings system tab on header item click", async ({ page }) => {
    const link = page.locator('.header a[aria-label="settings-system"]')
    await link.waitFor({ state: "visible" })
    await expect(link).toBeEnabled()
    await link.click()

    await expect(page).toHaveURL("/settings")

    const tab = page.locator('.page .block.settings .tabs .nav button[name="system"].active')
    await tab.waitFor({ state: "visible" })
    await expect(tab).toBeVisible()
  })
})