/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"

test.describe("Settings page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/settings", { waitUntil: "domcontentloaded" })
  })

  test("Should return 200 on general settings save", async ({ page }) => {
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

  test("Should return 400 on old password is missing", async ({ page }) => {
    await page.locator('.tabs .nav button[name="security"]').click()

    await page.locator('input[name="new-password"]').fill("wrong")
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("credentials") && resp.request().method() === "PATCH"
      ),
      page.locator('button[name="settings-save-security"]').click(),
    ])

    expect(response.status()).toBe(400)
  })

  test("Should return 204 on credentials update", async ({ page }) => {
    await page.locator('.tabs .nav button[name="security"]').click()

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("credentials") && resp.request().method() === "PATCH"
      ),
      page.locator('button[name="settings-save-security"]').click(),
    ])

    expect(response.status()).toBe(204)
  })

  test("Should return 204 on unused containers data clear", async ({ page }) => {
    await page.locator('.tabs .nav button[name="system"]').click()

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("containers") && resp.request().method() === "DELETE"
      ),
      page.locator('button[name="clear-containers"]').click(),
    ])

    expect(response.status()).toBe(204)
  })
})