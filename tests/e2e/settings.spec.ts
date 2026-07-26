/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"
import { gotoWithRetry, clickAndWaitForApi } from "./helpers/api.js"

test.describe("Settings page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/settings")
  })

  test("Should return 200 on general settings save", async ({ page }) => {
    const response = await clickAndWaitForApi(
      page,
      'button[name="settings-save-general"]',
      /settings/,
      "PATCH",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 409 on current password is invalid", async ({ page }) => {
    const securityTab = page.locator('.tabs .nav button[name="security"]')
    await securityTab.waitFor({ state: "visible" })
    await expect(securityTab).toBeEnabled()
    await securityTab.click()

    const oldPasswordInput = page.locator('input[name="old-password"]')
    await oldPasswordInput.waitFor({ state: "visible" })
    await oldPasswordInput.fill("wrong")

    const newPasswordInput = page.locator('input[name="new-password"]')
    await newPasswordInput.waitFor({ state: "visible" })
    await newPasswordInput.fill("wrong")

    const response = await clickAndWaitForApi(
      page,
      'button[name="settings-save-security"]',
      /credentials/,
      "PATCH",
    )
    expect(response.status()).toBe(409)
  })

  test("Should return 400 on old password is missing", async ({ page }) => {
    const securityTab = page.locator('.tabs .nav button[name="security"]')
    await securityTab.waitFor({ state: "visible" })
    await expect(securityTab).toBeEnabled()
    await securityTab.click()

    const newPasswordInput = page.locator('input[name="new-password"]')
    await newPasswordInput.waitFor({ state: "visible" })
    await newPasswordInput.fill("wrong")

    const response = await clickAndWaitForApi(
      page,
      'button[name="settings-save-security"]',
      /credentials/,
      "PATCH",
    )
    expect(response.status()).toBe(400)
  })

  test("Should return 204 on credentials update", async ({ page }) => {
    const securityTab = page.locator('.tabs .nav button[name="security"]')
    await securityTab.waitFor({ state: "visible" })
    await expect(securityTab).toBeEnabled()
    await securityTab.click()

    const response = await clickAndWaitForApi(
      page,
      'button[name="settings-save-security"]',
      /credentials/,
      "PATCH",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on unused containers data clear", async ({ page }) => {
    const systemTab = page.locator('.tabs .nav button[name="system"]')
    await systemTab.waitFor({ state: "visible" })
    await expect(systemTab).toBeEnabled()
    await systemTab.click()

    const response = await clickAndWaitForApi(
      page,
      'button[name="clear-containers"]',
      /containers/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })
})