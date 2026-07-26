/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, type Page, type Response } from "@playwright/test"
import { gotoWithRetry, clickAndWaitForApi } from "./helpers/api.js"

/**
 * Creates a server through the server-create popup.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: Name of the server to create.
 * - gameIndex: Index of the game option to select, or null to skip selection.
 * - selectLoader: Whether to select a loader option.
 * - selectVersion: Whether to select a version option.
 *
 * Returns:
 * - Promise<Response | undefined>: the API response for the create request,
 *   or undefined when the flow stops early due to missing selections.
 */
async function createServer(
  page: Page,
  name: string,
  gameIndex: number | null = 4,
  selectLoader: boolean = true,
  selectVersion: boolean = true,
): Promise<Response | undefined> {
  const createPopupButton = page.locator('button[name="server-create-popup"]')
  await createPopupButton.waitFor({ state: "visible" })
  await expect(createPopupButton).toBeEnabled()
  await createPopupButton.click()

  const nextStepButton = page.locator('button[name="server-next-step"]')

  if (gameIndex == null) {
    await nextStepButton.waitFor({ state: "visible" })
    await expect(nextStepButton).toBeEnabled()
    await nextStepButton.click()
    return
  }

  const gameOption = page.locator('div[aria-label="server-game"]').nth(gameIndex)
  await gameOption.waitFor({ state: "visible" })
  await gameOption.click()

  await nextStepButton.waitFor({ state: "visible" })
  await expect(nextStepButton).toBeEnabled()
  await nextStepButton.click()

  const createButton = page.locator('button[name="server-create"]')

  if (!name) {
    await createButton.waitFor({ state: "visible" })
    await expect(createButton).toBeEnabled()
    await createButton.click()
    return
  }

  const nameInput = page.locator('input[name="server-name"]')
  await nameInput.waitFor({ state: "visible" })
  await nameInput.fill(name)

  if (!selectLoader) {
    await createButton.waitFor({ state: "visible" })
    await expect(createButton).toBeEnabled()
    await createButton.click()
    return
  }

  const loaderField = page.locator('div[aria-label="server-loader"]')
  await loaderField.waitFor({ state: "visible" })
  await loaderField.click()

  const loaderDropdown = page.locator(".select-dropdown")
  await loaderDropdown.waitFor({ state: "visible" })
  await loaderDropdown.locator(".option").first().click()
  await loaderDropdown.waitFor({ state: "hidden" })

  if (!selectVersion) {
    await createButton.waitFor({ state: "visible" })
    await expect(createButton).toBeEnabled()
    await createButton.click()
    return
  }

  const versionField = page.locator('div[aria-label="server-version"]')
  await versionField.waitFor({ state: "visible" })
  await versionField.click()

  const versionDropdown = page.locator(".select-dropdown")
  await versionDropdown.waitFor({ state: "visible" })
  await versionDropdown.locator(".option").first().click()
  await versionDropdown.waitFor({ state: "hidden" })

  return clickAndWaitForApi(
    page,
    'button[name="server-create"]',
    /servers/,
    "POST",
  )
}

/**
 * Searches for a server by name.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: Server name to search for.
 *
 * Returns:
 * - Promise<Response>: the API response for the search request.
 */
async function searchServer(page: Page, name: string): Promise<Response> {
  const searchInput = page.locator('input[name="search-input"]')
  await searchInput.waitFor({ state: "visible" })
  await searchInput.fill(name)

  return clickAndWaitForApi(
    page,
    'button[name="search-submit"]',
    /servers/,
    "GET",
  )
}

test.describe.configure({ mode: "serial" })

test.describe("Servers page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/servers")
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

    const response = await clickAndWaitForApi(
      page,
      'button[name="search-reset"]',
      /servers/,
      "GET",
    )
    expect(response.status()).toBe(200)
  })
})