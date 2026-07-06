/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"

test.use({ storageState: { cookies: [], origins: [] } })

const TEST_USER = {
  login: process.env.TEST_LOGIN ?? "admin",
  password: process.env.TEST_PASSWORD ?? "admin",
}

test.describe("Login page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login", { waitUntil: "domcontentloaded" })
  })

  test("Should load login page", async ({ page }) => {
    await expect(page.locator("#app .page")).toBeVisible()
  })

  test("Should show validation warning on empty form", async ({ page }) => {
    await page.locator('button[name="sign-in"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on empty login", async ({ page }) => {
    await page.locator('input[name="password"]').fill(TEST_USER.password)
    await page.locator('button[name="sign-in"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on empty password", async ({ page }) => {
    await page.locator('input[name="login"]').fill(TEST_USER.login)
    await page.locator('button[name="sign-in"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 401 on invalid credentials", async ({ page }) => {
    await page.locator('input[name="login"]').fill("wrong")
    await page.locator('input[name="password"]').fill("wrong")
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("login") && resp.request().method() === "POST"
      ),
      page.locator('button[name="sign-in"]').click(),
    ])

    expect(response.status()).toBe(401)
  })

  test("Should sign in successfully", async ({ page }) => {
    await expect(page.getByText("Cobalt")).toBeVisible()

    await page.locator('input[name="login"]').fill(TEST_USER.login)
    await page.locator('input[name="password"]').fill(TEST_USER.password)
    await page.locator('button[name="sign-in"]').click()

    await expect(page).toHaveURL('/')
  })
})