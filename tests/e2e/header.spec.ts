/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"

test.describe("Header", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test("Should open Settings security tab on header item click", async ({ page }) => {
    await page.locator('.header a[aria-label="settings-security"]').click()

    await expect(page).toHaveURL("/settings")
    await expect(page.locator('.page .block.settings .tabs .nav button[name="security"].active')).toBeVisible()
  })

  test("Should open Settings system tab on header item click", async ({ page }) => {
    await page.locator('.header a[aria-label="settings-system"]').click()

    await expect(page).toHaveURL("/settings")
    await expect(page.locator('.page .block.settings .tabs .nav button[name="system"].active')).toBeVisible()
  })
})