/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"
import { gotoWithRetry } from "./helpers/api.js"

test.describe("Logout", () => {
  test("Should redirect to login page on logout", async ({ browser }) => {
    const context = await browser.newContext({
      storageState: ".auth/session.json",
    })
    const page = await context.newPage()
    await gotoWithRetry(page, "/")

    const logoutButton = page.locator('.menu button[name="logout"]')
    await logoutButton.waitFor({ state: "visible" })
    await expect(logoutButton).toBeEnabled()
    await logoutButton.click()

    await expect(page).toHaveURL(/\/login/)
    await context.close()
  })
})