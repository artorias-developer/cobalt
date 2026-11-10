/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { Page } from "@playwright/test"
import { test, expect, newSignedInPage, TEST_USER } from "./helpers/fixtures.js"
import { gotoWithRetry, clickAndWaitForApi } from "./helpers/api.js"

test.describe.configure({ mode: "default" })

/**
 * Logs out through the menu button.
 *
 * Parameters:
 * - page: Playwright page instance.
 *
 * Returns:
 * - Promise<void>.
 */
async function logout(page: Page): Promise<void> {
  const logoutButton = page.locator('.menu button[name="logout"]')
  await logoutButton.waitFor({ state: "visible" })
  await expect(logoutButton).toBeEnabled()
  await logoutButton.click()
}

/**
 * Opens the system tab of the settings page.
 *
 * Parameters:
 * - page: Playwright page instance.
 *
 * Returns:
 * - Promise<void>.
 */
async function openSystemTab(page: Page): Promise<void> {
  await gotoWithRetry(page, "/settings")

  const systemTab = page.locator('.tabs .nav button[name="system"]')
  await systemTab.waitFor({ state: "visible" })
  await expect(systemTab).toBeEnabled()
  await systemTab.click()
}

test.describe("Logout", () => {
  test("Should open Login page on logout", async ({ browser }) => {
    const page = await newSignedInPage(browser, TEST_USER.login, TEST_USER.password)
    await gotoWithRetry(page, "/")

    await logout(page)

    await expect(page).toHaveURL(/\/login/)
    await page.context().close()
  })

  test("Should open Login page on dashboard page open after logout", async ({ browser }) => {
    const page = await newSignedInPage(browser, TEST_USER.login, TEST_USER.password)
    await gotoWithRetry(page, "/")

    await logout(page)
    await expect(page).toHaveURL(/\/login/)

    await gotoWithRetry(page, "/")
    await expect(page).toHaveURL(/\/login/)
    await page.context().close()
  })
})

test.describe("Settings page system tab", () => {
  test("Should return 204 on containers clear", async ({ page }) => {
    await openSystemTab(page)

    const response = await clickAndWaitForApi(
      page,
      'button[name="clear-containers"]',
      /containers/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on cache clear", async ({ page }) => {
    await openSystemTab(page)

    const response = await clickAndWaitForApi(
      page,
      'button[name="clear-cache"]',
      /cache/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })
})
