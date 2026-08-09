/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test as setup, expect } from "@playwright/test"
import { gotoWithRetry } from "./api.js"

const TEST_USER = {
  login: process.env.TEST_LOGIN ?? "admin",
  password: process.env.TEST_PASSWORD ?? "admin",
}

setup("Authenticate", async ({ page }) => {
  await gotoWithRetry(page, "/login")

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

  await page.waitForURL("/")

  await page.context().storageState({ path: ".auth/session.json" })
})