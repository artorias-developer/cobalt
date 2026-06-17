/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, type Page, type Response } from "@playwright/test"

async function createServer(
  page: Page,
  name: string,
  gameIndex: number | null = 4,
  selectLoader: boolean = true,
  selectVersion: boolean = true,
): Promise<Response | undefined> {
  await page.locator('button[name="server-create-popup"]').click()

  if (gameIndex == null) {
    await page.locator('button[name="server-next-step"]').click()
    return
  }

  await page.locator('div[aria-label="server-game"]').nth(gameIndex).click()
  await page.locator('button[name="server-next-step"]').click()

  if (!name) {
    await page.locator('button[name="server-create"]').click()
    return
  }

  await page.locator('input[name="server-name"]').fill(name)

  if (!selectLoader) {
    await page.locator('button[name="server-create"]').click()
    return
  }

  await page.locator('div[aria-label="server-loader"]').click()
  await page.locator(".select-dropdown .option").first().waitFor()
  await page.waitForTimeout(700)
  await page.locator(".select-dropdown .option").first().click()

  if (!selectVersion) {
    await page.locator('button[name="server-create"]').click()
    return
  }

  await page.locator('div[aria-label="server-version"]').click()
  await page.locator(".select-dropdown .option").first().waitFor()
  await page.waitForTimeout(700)
  await page.locator(".select-dropdown .option").first().click()

  const [response] = await Promise.all([
    page.waitForResponse((resp) =>
      resp.url().includes("servers") && resp.request().method() === "POST"
    ),
    page.locator('button[name="server-create"]').click(),
  ])
  return response
}

async function searchServer(page: Page, name: string): Promise<Response> {
  await page.locator('input[name="search-input"]').fill(name)
  const [response] = await Promise.all([
    page.waitForResponse((resp) =>
      resp.url().includes("servers") && resp.request().method() === "GET"
    ),
    page.locator('button[name="search-submit"]').click(),
  ])
  return response
}

test.describe.configure({ mode: "serial" })

test.describe("Servers page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/servers", { waitUntil: "domcontentloaded" })
  })

  test("Should show validation warning on unselected game", async ({ page }) => {
    await createServer(page, "e2e_test_server", null)
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on empty server name", async ({ page }) => {
    await createServer(page, "")
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on unselected loader", async ({ page }) => {
    await createServer(
      page,
      "e2e_test_server",
      4,
      false,
    )
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on unselected version", async ({ page }) => {
    await createServer(
      page,
      "e2e_test_server",
      4,
      true,
      false,
    )
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show server settings button on server create", async ({ page }) => {
    test.setTimeout(185000)
    const response = await createServer(page, "e2e_test_server")
    expect(response!.status()).toBe(200)

    const row = page.locator("tr").filter({
      has: page.locator("td", { hasText: "e2e_test_server" }),
    })

    await expect(
      row.locator('a[aria-label="server-settings"], .status-icon .icon.red')
    ).toBeVisible({ timeout: 180000 })

    await expect(row.locator(".status-icon .icon.red")).not.toBeVisible()
    await expect(row.locator('a[aria-label="server-settings"]')).toBeVisible()
  })

  test("Should return 200 on server search", async ({ page }) => {
    const response = await searchServer(page, "e2e_test_server")
    expect(response.status()).toBe(200)
  })

  test("Should return 404 on fictional server search", async ({ page }) => {
    const response = await searchServer(page, "fictional_server")
    expect(response.status()).toBe(404)
  })

  test("Should return 200 on search reset", async ({ page }) => {
    await searchServer(page, "e2e_test_server")
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("servers") && resp.request().method() === "GET"
      ),
      page.locator('button[name="search-reset"]').click(),
    ])

    expect(response.status()).toBe(200)
  })
})
