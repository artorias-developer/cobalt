/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, newSignedInPage } from "./helpers/fixtures.js"
import { gotoWithRetry, clickAndWaitForApi } from "./helpers/api.js"

test.describe("Dashboard page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/")
  })

  for (const block of ["cpu", "ram", "disk", "logs"]) {
    test(`Should show ${block} block on dashboard page open`, async ({ page }) => {
      await expect(page.locator(`.page .block.${block}`)).toBeVisible()
    })
  }

  test("Should return 200 on disk metrics reload", async ({ page }) => {
    const response = await clickAndWaitForApi(
      page,
      '.block.disk button[name="reload"]',
      /disk/,
      "GET",
    )
    expect(response.status()).toBe(200)
  })

  test("Should hide disk metrics reload on dashboard page open with restricted role", async ({ api, browser }) => {
    const role = await api.createRole(undefined, ["dashboard_view"])
    const user = await api.createUser(undefined, role.id)

    const userPage = await newSignedInPage(browser, user.login, user.password)
    await gotoWithRetry(userPage, "/")

    await expect(userPage.locator(".page .block.disk")).toBeVisible()
    await expect(userPage.locator('.block.disk button[name="reload"]')).toHaveCount(0)
    await userPage.context().close()
  })
})
