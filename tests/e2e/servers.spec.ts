/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { Page, Response } from "@playwright/test"
import { test, expect, uniqueName, newSignedInPage } from "./helpers/fixtures.js"
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

/**
 * Opens a server row action after narrowing the table down by search,
 * so the row is found regardless of pagination.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: Server name.
 * - action: Row action button name (e.g. "server-edit-popup").
 *
 * Returns:
 * - Promise<void>.
 */
async function openServerAction(page: Page, name: string, action: string): Promise<void> {
  await searchServer(page, name)

  const row = page.locator("tr").filter({
    has: page.locator("td", { hasText: name }),
  })
  const button = row.locator(`[name="${action}"]`)
  await button.waitFor({ state: "visible" })
  await expect(button).toBeEnabled()
  await button.click()
}

/**
 * Changes the name in the opened server-edit popup and submits it.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: New server name.
 *
 * Returns:
 * - Promise<Response>: the API response for the update request.
 */
async function updateServerName(page: Page, name: string): Promise<Response> {
  const nameInput = page.locator('.edit-server-popup input[name="server-name"]')
  await nameInput.waitFor({ state: "visible" })
  await nameInput.fill(name)

  return clickAndWaitForApi(
    page,
    'button[name="server-update"]',
    /servers/,
    "PATCH",
  )
}

test.describe("Servers page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/servers")
  })

  test("Should show validation warning on server create with unselected game", async ({ page }) => {
    await createServer(page, uniqueName("server"), null)
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on server create with empty name", async ({ page }) => {
    await createServer(page, "")
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on server create with unselected loader", async ({ page }) => {
    await createServer(page, uniqueName("server"), 4, false)
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on server create with unselected version", async ({ page }) => {
    await createServer(page, uniqueName("server"), 4, true, false)
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show server settings button on server create", async ({ api, browser }) => {
    test.setTimeout(100_000)

    const role = await api.createRole(undefined, ["servers_view", "servers_create", "server_view", "games_view"])
    const user = await api.createUser(undefined, role.id)

    const page = await newSignedInPage(browser, user.login, user.password)
    await gotoWithRetry(page, "/servers")

    const name = uniqueName("server")
    api.track("servers", name)

    const response = await createServer(page, name)
    expect(response!.status()).toBe(200)

    const row = page.locator("tr").filter({
      has: page.locator("td", { hasText: name }),
    })

    await expect(
      row.locator('a[aria-label="server-settings"], .status-icon .icon.red')
    ).toBeVisible({ timeout: 90_000 })

    await expect(row.locator(".status-icon .icon.red")).not.toBeVisible()
    await expect(row.locator('a[aria-label="server-settings"]')).toBeVisible()
    await page.context().close()
  })

  test("Should return 409 on server create with existing name", async ({ page, server }) => {
    const response = await createServer(page, server.name)
    expect(response!.status()).toBe(409)
  })

  test("Should return 200 on server search", async ({ page, server }) => {
    const response = await searchServer(page, server.name)
    expect(response.status()).toBe(200)
  })

  test("Should return 404 on server search with fictional name", async ({ page }) => {
    const response = await searchServer(page, "fictional_server")
    expect(response.status()).toBe(404)
  })

  test("Should return 200 on server search reset", async ({ page, server }) => {
    await searchServer(page, server.name)

    const response = await clickAndWaitForApi(
      page,
      'button[name="search-reset"]',
      /servers/,
      "GET",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 200 on server update", async ({ page, api }) => {
    const server = await api.createServer()
    await openServerAction(page, server.name, "server-edit-popup")

    const response = await updateServerName(page, `${server.name}_updated`)
    expect(response.status()).toBe(200)
  })

  test("Should return 409 on server update with existing name", async ({ page, api, server }) => {
    const own = await api.createServer()
    await openServerAction(page, own.name, "server-edit-popup")

    const response = await updateServerName(page, server.name)
    expect(response.status()).toBe(409)
  })

  test("Should return 204 on server delete", async ({ page, api }) => {
    const server = await api.createServer()
    await openServerAction(page, server.name, "server-delete-popup")

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /\/servers\/\d+(\?|$)/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })
})
