/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test as setup } from "@playwright/test"

const TEST_USER = {
  login: process.env.TEST_LOGIN ?? "admin",
  password: process.env.TEST_PASSWORD ?? "admin",
}

setup("authenticate", async ({ page }) => {
  await page.goto("/login")

  await page.locator('input[name="login"]').fill(TEST_USER.login)
  await page.locator('input[name="password"]').fill(TEST_USER.password)
  await page.locator('button[name="sign-in"]').click()
  await page.waitForURL('/')

  await page.context().storageState({ path: ".auth/session.json" })
})