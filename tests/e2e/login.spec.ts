/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"
import { gotoWithRetry, clickAndWaitForApi } from "./helpers/api.js"

test.use({ storageState: { cookies: [], origins: [] } })

const TEST_USER = {
  login: process.env.TEST_LOGIN ?? "admin",
  password: process.env.TEST_PASSWORD ?? "admin",
}

test.describe("Login page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/login")
  })

  test("Should load login page", async ({ page }) => {
    const app = page.locator("#app .page")
    await app.waitFor({ state: "visible" })
    await expect(app).toBeVisible()
  })

  test("Should show validation warning on empty form", async ({ page }) => {
    const signInButton = page.locator('button[name="sign-in"]')
    await signInButton.waitFor({ state: "visible" })
    await expect(signInButton).toBeEnabled()
    await signInButton.click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on empty login", async ({ page }) => {
    const passwordInput = page.locator('input[name="password"]')
    await passwordInput.waitFor({ state: "visible" })
    await passwordInput.fill(TEST_USER.password)

    const signInButton = page.locator('button[name="sign-in"]')
    await signInButton.waitFor({ state: "visible" })
    await expect(signInButton).toBeEnabled()
    await signInButton.click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on empty password", async ({ page }) => {
    const loginInput = page.locator('input[name="login"]')
    await loginInput.waitFor({ state: "visible" })
    await loginInput.fill(TEST_USER.login)

    const signInButton = page.locator('button[name="sign-in"]')
    await signInButton.waitFor({ state: "visible" })
    await expect(signInButton).toBeEnabled()
    await signInButton.click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 401 on invalid credentials", async ({ page }) => {
    const loginInput = page.locator('input[name="login"]')
    await loginInput.waitFor({ state: "visible" })
    await loginInput.fill("wrong")

    const passwordInput = page.locator('input[name="password"]')
    await passwordInput.waitFor({ state: "visible" })
    await passwordInput.fill("wrong")

    const response = await clickAndWaitForApi(
      page,
      'button[name="sign-in"]',
      /login/,
      "POST",
    )
    expect(response.status()).toBe(401)
  })

  test("Should sign in successfully", async ({ page }) => {
    await expect(page.getByText("Cobalt")).toBeVisible()

    const loginInput = page.locator('input[name="login"]')
    await loginInput.waitFor({ state: "visible" })
    await loginInput.fill(TEST_USER.login)

    const passwordInput = page.locator('input[name="password"]')
    await passwordInput.waitFor({ state: "visible" })
    await passwordInput.fill(TEST_USER.password)

    const signInButton = page.locator('button[name="sign-in"]')
    await signInButton.waitFor({ state: "visible" })
    await expect(signInButton).toBeEnabled()
    await signInButton.click()

    await expect(page).toHaveURL("/")
  })
})