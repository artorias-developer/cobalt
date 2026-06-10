/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"

test.describe("Logout", () => {
  test("Should redirect to login page on logout", async ({ browser }) => {
    const context = await browser.newContext({
      storageState: ".auth/session.json",
    })
    const page = await context.newPage()
    await page.goto('/', { waitUntil: "domcontentloaded" })

    await page.locator('.menu button[name="logout"]').click()

    await expect(page).toHaveURL(/\/login/)
    await context.close()
  })
})