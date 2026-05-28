/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, Page } from "@playwright/test"

test.use({ storageState: { cookies: [], origins: [] } })

export const TEST_USER = {
  login: process.env.TEST_LOGIN ?? "admin",
  password: process.env.TEST_PASSWORD ?? "admin",
}

async function fillLoginForm(
  page: Page,
  login: string,
  password: string
): Promise<void> {
  await page.locator('input[name="login"]').fill(login)
  await page.locator('input[name="password"]').fill(password)
}

test.describe("Login page", () => {
  test("Should show validation warning on empty form", async ({ page }) => {
    await page.goto("/login")

    await page.locator('button[name="sign-in"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 401 on invalid credentials", async ({ page }) => {
    await page.goto("/login")

    await fillLoginForm(page, "wrong", "wrong")
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("login") && resp.request().method() === "POST"
      ),
      page.locator('button[name="sign-in"]').click(),
    ])

    expect(response.status()).toBe(401)
  })

  test("Should sign in successfully", async ({ page }) => {
    await page.goto("/login")

    await expect(page.getByText("Cobalt")).toBeVisible()

    await fillLoginForm(page, TEST_USER.login, TEST_USER.password)
    await page.locator('button[name="sign-in"]').click()

    await expect(page).toHaveURL('/')
  })
})