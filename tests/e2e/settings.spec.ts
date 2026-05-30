/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"

test.describe("Settings page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/settings")
  })

  test("Should save general settings successfully", async ({ page }) => {
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("settings") && resp.request().method() === "PATCH"
      ),
      page.locator('button[name="settings-save-general"]').click(),
    ])

    expect(response.status()).toBe(200)
  })

  test("Should return 409 on current password is invalid", async ({ page }) => {
    await page.locator('.tabs .nav button[name="security"]').click()

    await page.locator('input[name="old-password"]').fill("wrong")
    await page.locator('input[name="new-password"]').fill("wrong")
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("credentials") && resp.request().method() === "PATCH"
      ),
      page.locator('button[name="settings-save-security"]').click(),
    ])

    expect(response.status()).toBe(409)
  })

  test("Should return 400 on one of the password is missing", async ({ page }) => {
    await page.locator('.tabs .nav button[name="security"]').click()

    await page.locator('input[name="old-password"]').fill("wrong")
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("credentials") && resp.request().method() === "PATCH"
      ),
      page.locator('button[name="settings-save-security"]').click(),
    ])

    expect(response.status()).toBe(400)
  })

  test("Should update credentials successfully", async ({ page }) => {
    await page.locator('.tabs .nav button[name="security"]').click()

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("credentials") && resp.request().method() === "PATCH"
      ),
      page.locator('button[name="settings-save-security"]').click(),
    ])

    expect(response.status()).toBe(204)
  })
})