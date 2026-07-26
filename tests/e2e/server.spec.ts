/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, type Page, type Response } from "@playwright/test"
import { gotoWithRetry, waitForApi, clickAndWaitForApi } from "./helpers/api.js"


/**
 * Creates a file or directory through the file-create popup.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: Name of the file or directory to create.
 * - type: "file" | "directory" - entry type to create.
 *
 * Returns:
 * - Promise<Response>: the API response for the create request.
 */
async function createFile(
  page: Page,
  name: string,
  type: "file" | "directory" = "file",
): Promise<Response> {
  await page.locator('button[name="file-create-popup"]').click()
  await page.locator('input[name="file-name"]').fill(name)
  await page.locator('div[aria-label="file-type"]').click()

  const dropdownOption = page.locator(".select-dropdown .option").first()
  await dropdownOption.waitFor({ state: "visible" })

  await page
    .locator(`.select-dropdown .option .value[aria-label="${type}"]`)
    .click()

  return clickAndWaitForApi(
    page,
    'button[name="file-create"]',
    /\/files(\/|$|\?)/,
    "POST",
  )
}

/**
 * Finds a table row by file or directory name.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: File or directory name to locate.
 *
 * Returns:
 * - Locator: locator for the matching row.
 */
async function getFileRow(page: Page, name: string) {
  return page.locator("tr").filter({
    has: page.locator("td", { hasText: name }),
  })
}

/**
 * Opens the actions menu for a given file row.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: File or directory name.
 *
 * Returns:
 * - Promise<void>.
 */
async function openFileActions(page: Page, name: string) {
  const row = await getFileRow(page, name)
  await row.locator(".actions-button .trigger").click()
}

/**
 * Selects a file row via its checkbox.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: File or directory name.
 *
 * Returns:
 * - Promise<void>.
 */
async function selectFile(page: Page, name: string) {
  const row = await getFileRow(page, name)
  await row.locator("td .label-checkbox .checkbox").click()
}

/**
 * Navigates to a server's settings page.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - serverName: Name of the server to open.
 *
 * Returns:
 * - Promise<void>.
 */
async function openServerSettings(page: Page, serverName: string) {
  await gotoWithRetry(page, "/servers")

  const row = page.locator("tr").filter({
    has: page.locator("td", { hasText: serverName }),
  })
  await row.waitFor({ state: "visible" })

  await row.locator('a[aria-label="server-settings"]').click()

  const tabsNav = page.locator(".tabs .nav").filter({
    has: page.locator('button[name="files"]'),
  })
  await tabsNav.waitFor({ state: "visible" })
}

/**
 * Navigates to a server's settings page and opens the files tab.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - serverName: Name of the server to open.
 *
 * Returns:
 * - Promise<void>.
 */
async function openFilesTab(page: Page, serverName: string) {
  await openServerSettings(page, serverName)

  const tabsNav = page.locator(".tabs .nav").filter({
    has: page.locator('button[name="files"]'),
  })
  await tabsNav.locator('button[name="files"]').click()
  await page.locator("table tbody").waitFor({ state: "visible" })
}

test.describe.configure({ mode: "serial" })

test.describe("Server files", () => {
  test.beforeEach(async ({ page }) => {
    await openFilesTab(page, "e2e_test_server")
  })

  test("Should show warning on empty name at file create", async ({ page }) => {
    await page.locator('button[name="file-create-popup"]').click()
    await page.locator('button[name="file-create"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 204 on files and directory create", async ({ page }) => {
    const response1 = await createFile(page, "e2e_test_file.txt")
    expect(response1.status()).toBe(204)

    const response2 = await createFile(page, "e2e_test_file2.txt")
    expect(response2.status()).toBe(204)

    const response3 = await createFile(page, "e2e_test_dir", "directory")
    expect(response3.status()).toBe(204)
  })

  test("Should return 409 on file create with existing name", async ({ page }) => {
    const response = await createFile(page, "e2e_test_file.txt")
    expect(response.status()).toBe(409)
  })

  test("Should return 200 on reload", async ({ page }) => {
    const response = await clickAndWaitForApi(
      page,
      'button[name="file-reload-popup"]',
      /\/files(\/|$|\?)/,
      "GET",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 204 on file open and save", async ({ page }) => {
    await openFileActions(page, "e2e_test_file.txt")
    await page.locator('button[name="file-open"]').click()

    const response = await clickAndWaitForApi(
      page,
      'button[name="file-save"]',
      /\/files(\/|$|\?)/,
      "PUT",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file rename", async ({ page }) => {
    await openFileActions(page, "e2e_test_file.txt")
    await page.locator('button[name="file-rename-popup"]').click()
    await page.locator('input[name="file-name"]').fill("e2e_test_file_renamed.txt")

    const response = await clickAndWaitForApi(
      page,
      'button[name="file-rename"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 409 on file rename to existing name", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="file-rename-popup"]').click()
    await page.locator('input[name="file-name"]').fill("e2e_test_file2.txt")

    const response = await clickAndWaitForApi(
      page,
      'button[name="file-rename"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(409)
  })

  test("Should return 200 on file download via actions menu", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")

    const response = await clickAndWaitForApi(
      page,
      'button[name="file-download"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 200 on file download via footer", async ({ page }) => {
    await selectFile(page, "e2e_test_file_renamed.txt")

    const response = await clickAndWaitForApi(
      page,
      'button[name="files-download"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 204 on file duplicate via actions menu", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")

    const response = await clickAndWaitForApi(
      page,
      'button[name="file-duplicate"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file duplicate via footer", async ({ page }) => {
    await selectFile(page, "e2e_test_file_renamed.txt")

    const response = await clickAndWaitForApi(
      page,
      'button[name="files-duplicate"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should show warning on empty destination at file move via actions menu", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="file-move-popup"]').click()
    await page.locator('button[name="file-move"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show warning on empty destination at file move via footer", async ({ page }) => {
    await selectFile(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="files-move-popup"]').click()
    await page.locator('button[name="file-move"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 204 on file move via actions menu", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="file-move-popup"]').click()
    await page.locator('input[name="file-move-destination"]').fill("/e2e_test_dir")

    const response = await clickAndWaitForApi(
      page,
      'button[name="file-move"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file move via footer", async ({ page }) => {
    const dirRow = await getFileRow(page, "e2e_test_dir")
    await dirRow.locator("td").nth(1).click()

    await selectFile(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="files-move-popup"]').click()
    await page.locator('input[name="file-move-destination"]').fill("/")

    const response = await clickAndWaitForApi(
      page,
      'button[name="file-move"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 404 on file move to non-existing directory via actions menu", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="file-move-popup"]').click()
    await page.locator('input[name="file-move-destination"]').fill("/fictional_dir")

    const response = await clickAndWaitForApi(
      page,
      'button[name="file-move"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(404)
  })

  test("Should return 404 on file move to non-existing directory via footer", async ({ page }) => {
    await selectFile(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="files-move-popup"]').click()
    await page.locator('input[name="file-move-destination"]').fill("/fictional_dir")

    const response = await clickAndWaitForApi(
      page,
      'button[name="file-move"]',
      /\/files(\/|$|\?)/,
      "POST",
    )
    expect(response.status()).toBe(404)
  })

  test("Should show one row on file search", async ({ page }) => {
    await page.locator('input[name="search-input"]').fill("e2e_test_file_renamed.txt")
    await page.locator('button[name="search-submit"]').click()

    const rows = page.locator("tbody tr")
    await expect(rows).toHaveCount(1)
    await expect(rows.first().locator("td", { hasText: "e2e_test_file_renamed.txt" })).toBeVisible()
  })

  test("Should show empty table on fictional file search", async ({ page }) => {
    await page.locator('input[name="search-input"]').fill("fictional_file")
    await page.locator('button[name="search-submit"]').click()

    const rows = page.locator("tbody tr")
    await expect(rows).toHaveCount(0)
  })

  test("Should return 204 on file delete via actions menu", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="file-delete-popup"]').click()

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /\/files(\/|$|\?)/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file delete via footer", async ({ page }) => {
    await selectFile(page, "e2e_test_file2.txt")
    await page.locator('button[name="files-delete-popup"]').click()

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /\/files(\/|$|\?)/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on directory delete", async ({ page }) => {
    await openFileActions(page, "e2e_test_dir")
    await page.locator('button[name="file-delete-popup"]').click()

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /\/files(\/|$|\?)/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })
})

test.describe("Server overview", () => {
  test.beforeEach(async ({ page }) => {
    await openServerSettings(page, "e2e_test_server")
  })

  test("Should return 204 on console command", async ({ page }) => {
    const consoleInput = page.locator('input[name="server-console"]')
    await consoleInput.waitFor({ state: "visible" })
    await expect(consoleInput).toBeEnabled()

    const responsePromise = waitForApi(
        page,
        /\/servers\/\d+\/execute(\?|$)/,
        "POST"
    )

    await consoleInput.fill("/help")
    await consoleInput.press("Enter")

    const response = await responsePromise
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on server stop", async ({ page }) => {
    const response = await clickAndWaitForApi(
      page,
      'button[name="server-stop"]',
      /\/servers\/\d+\/stop(\?|$)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 500 on console command when server is stopped", async ({ page }) => {
    const consoleInput = page.locator('input[name="server-console"]')
    await consoleInput.waitFor({ state: "visible" })
    await expect(consoleInput).toBeEnabled()

    const responsePromise = waitForApi(
        page,
        /\/servers\/\d+\/execute(\?|$)/,
        "POST"
    )

    await consoleInput.fill("/help")
    await consoleInput.press("Enter")

    const response = await responsePromise
    expect(response.status()).toBe(500)
  })

  test("Should return 204 on server start", async ({ page }) => {
    const response = await clickAndWaitForApi(
      page,
      'button[name="server-start"]',
      /\/servers\/\d+\/start(\?|$)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on server restart", async ({ page }) => {
    const response = await clickAndWaitForApi(
      page,
      'button[name="server-restart"]',
      /\/servers\/\d+\/restart(\?|$)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })
})

test.describe("Servers page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/servers")
    await page.locator("table tbody").waitFor({ state: "visible" })
  })

  test("Should return 204 on server delete", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td", { hasText: "e2e_test_server" }),
    })
    await row.locator('button[name="server-delete-popup"]').click()

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /\/servers\/\d+(\?|$)/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })
})