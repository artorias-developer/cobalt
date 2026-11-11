/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "./helpers/fixtures.js"
import { gotoWithRetry } from "./helpers/api.js"

const ROUTES = [
  { path: "/", crumb: "Dashboard" },
  { path: "/servers", crumb: "Servers" },
  { path: "/users", crumb: "Users" },
  { path: "/roles", crumb: "Roles" },
  { path: "/settings", crumb: "Settings" },
]

test.describe("Header", () => {
  test("Should open Settings security tab on header item click", async ({ page }) => {
    await gotoWithRetry(page, "/")

    const link = page.locator('.header a[aria-label="settings-security"]')
    await link.waitFor({ state: "visible" })
    await expect(link).toBeEnabled()
    await link.click()

    await expect(page).toHaveURL(/\/settings/)
    await expect(page.locator('.page .block.settings .tabs .nav button[name="security"].active')).toBeVisible()
  })

  test("Should open Settings system tab on header item click", async ({ page }) => {
    await gotoWithRetry(page, "/")

    const link = page.locator('.header a[aria-label="settings-system"]')
    await link.waitFor({ state: "visible" })
    await expect(link).toBeEnabled()
    await link.click()

    await expect(page).toHaveURL(/\/settings/)
    await expect(page.locator('.page .block.settings .tabs .nav button[name="system"].active')).toBeVisible()
  })

  for (const { path, crumb } of ROUTES) {
    test(`Should show ${crumb} crumb in breadcrumbs on ${crumb} page open`, async ({ page }) => {
      await gotoWithRetry(page, path)
      await expect(page.locator(".header .breadcrumbs .crumb.current")).toHaveText(crumb)
    })
  }

  test("Should show Not Found crumb in breadcrumbs on unknown page open", async ({ page }) => {
    await gotoWithRetry(page, "/e2e-unknown-page")
    await expect(page.locator(".header .breadcrumbs .crumb.current")).toHaveText("Not Found")
  })
})
