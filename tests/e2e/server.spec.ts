/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { Page, Response } from "@playwright/test"
import { test, expect, uniqueFileName, type ServerData } from "./helpers/fixtures.js"
import { gotoWithRetry, waitForApi, clickAndWaitForApi, createZip } from "./helpers/api.js"

const FILES_API = /\/files(\/|$|\?)/

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
    FILES_API,
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
 * Opens the server page directly by its URL.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - server: Server to open.
 *
 * Returns:
 * - Promise<void>.
 */
async function openServerPage(page: Page, server: ServerData): Promise<void> {
  await gotoWithRetry(page, `/servers/${server.gameName}/${server.id}`)

  const tabsNav = page.locator(".tabs .nav").filter({
    has: page.locator('button[name="files"]'),
  })
  await tabsNav.waitFor({ state: "visible" })
}

/**
 * Opens the server page and switches to the files tab.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - server: Server to open.
 *
 * Returns:
 * - Promise<void>.
 */
async function openFilesTab(page: Page, server: ServerData): Promise<void> {
  await openServerPage(page, server)

  const tabsNav = page.locator(".tabs .nav").filter({
    has: page.locator('button[name="files"]'),
  })
  await tabsNav.locator('button[name="files"]').click()
  await page.locator("table tbody").waitFor({ state: "visible" })
}

/**
 * Opens a directory by clicking its row.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: Directory name.
 *
 * Returns:
 * - Promise<void>.
 */
async function openDirectory(page: Page, name: string): Promise<void> {
  const row = await getFileRow(page, name)
  await row.locator("td").nth(1).click()
}

/**
 * Fills the move popup destination and submits it.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - destination: Destination directory path.
 *
 * Returns:
 * - Promise<Response>: the API response for the move request.
 */
async function submitMove(page: Page, destination: string): Promise<Response> {
  await page.locator('input[name="file-move-destination"]').fill(destination)
  return clickAndWaitForApi(page, 'button[name="file-move"]', FILES_API, "POST")
}

/**
 * Sends a server command through the console input.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - command: Command to send.
 *
 * Returns:
 * - Promise<Response>: the API response for the execute request.
 */
async function sendServerCommand(page: Page, command: string): Promise<Response> {
  const consoleInput = page.locator('input[name="server-console"]')
  await consoleInput.waitFor({ state: "visible" })
  await expect(consoleInput).toBeEnabled()

  const responsePromise = waitForApi(page, /\/servers\/\d+\/execute(\?|$)/, "POST")
  await consoleInput.fill(command)
  await consoleInput.press("Enter")
  return responsePromise
}

test.describe("Server page files tab", () => {
  test("Should show validation warning on file create with empty name", async ({ page, server }) => {
    await openFilesTab(page, server)

    await page.locator('button[name="file-create-popup"]').click()
    await page.locator('button[name="file-create"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 204 on file create", async ({ page, server }) => {
    const file = uniqueFileName("file.txt")

    await openFilesTab(page, server)

    const response = await createFile(page, file)
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on directory create", async ({ page, server }) => {
    const dir = uniqueFileName("dir")

    await openFilesTab(page, server)

    const response = await createFile(page, dir, "directory")
    expect(response.status()).toBe(204)
  })

  test("Should return 409 on file create with existing name", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    const response = await createFile(page, file)
    expect(response.status()).toBe(409)
  })

  test("Should return 204 on file upload", async ({ page, server }) => {
    const upload = uniqueFileName("upload.txt")

    await openFilesTab(page, server)

    await page.locator('button[name="file-upload-popup"]').click()
    await page.locator('.upload-file-popup input[type="file"]').setInputFiles({
      name: upload,
      mimeType: "text/plain",
      buffer: Buffer.from("e2e"),
    })

    const response = await clickAndWaitForApi(
      page,
      '.upload-file-popup button[type="submit"]',
      FILES_API,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 200 on files reload", async ({ page, server }) => {
    await openFilesTab(page, server)

    const response = await clickAndWaitForApi(page, 'button[name="file-reload-popup"]', FILES_API, "GET")
    expect(response.status()).toBe(200)
  })

  test("Should show directory content on directory open", async ({ page, api, server }) => {
    const nested = uniqueFileName("nested.txt")
    const dir = uniqueFileName("dir")

    await api.createFile(server.id, `/${dir}`, "directory")
    await api.createFile(server.id, `/${dir}/${nested}`)
    await openFilesTab(page, server)

    await openDirectory(page, dir)

    await expect(await getFileRow(page, nested)).toBeVisible()
  })

  test("Should return 204 on file save", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await openFileActions(page, file)
    await page.locator('button[name="file-open"]').click()

    const response = await clickAndWaitForApi(page, 'button[name="file-save"]', FILES_API, "PUT")
    expect(response.status()).toBe(204)
  })

  test("Should show files table on file editor close", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await openFileActions(page, file)
    await page.locator('button[name="file-open"]').click()
    await expect(page.locator(".editor")).toBeVisible()

    await page.locator('button[name="file-close"]').click()

    await expect(page.locator(".editor")).not.toBeVisible()
    await expect(await getFileRow(page, file)).toBeVisible()
  })

  test("Should return 204 on file rename", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")
    const renamed = uniqueFileName("file_renamed.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await openFileActions(page, file)
    await page.locator('button[name="file-rename-popup"]').click()
    await page.locator('input[name="file-name"]').fill(renamed)

    const response = await clickAndWaitForApi(page, 'button[name="file-rename"]', FILES_API, "POST")
    expect(response.status()).toBe(204)
  })

  test("Should return 409 on file rename with existing name", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")
    const otherFile = uniqueFileName("file2.txt")

    await api.createFile(server.id, `/${file}`)
    await api.createFile(server.id, `/${otherFile}`)
    await openFilesTab(page, server)

    await openFileActions(page, file)
    await page.locator('button[name="file-rename-popup"]').click()
    await page.locator('input[name="file-name"]').fill(otherFile)

    const response = await clickAndWaitForApi(page, 'button[name="file-rename"]', FILES_API, "POST")
    expect(response.status()).toBe(409)
  })

  test("Should return 200 on file download via actions menu", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await openFileActions(page, file)

    const response = await clickAndWaitForApi(page, 'button[name="file-download"]', FILES_API, "POST")
    expect(response.status()).toBe(200)
  })

  test("Should return 200 on file download via footer", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await selectFile(page, file)

    const response = await clickAndWaitForApi(page, 'button[name="files-download"]', FILES_API, "POST")
    expect(response.status()).toBe(200)
  })

  test("Should return 204 on file duplicate via actions menu", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await openFileActions(page, file)

    const response = await clickAndWaitForApi(page, 'button[name="file-duplicate"]', FILES_API, "POST")
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file duplicate via footer", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await selectFile(page, file)

    const response = await clickAndWaitForApi(page, 'button[name="files-duplicate"]', FILES_API, "POST")
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on archive extract", async ({ page, api, server }) => {
    const archive = uniqueFileName("archive.zip")
    const extracted = uniqueFileName("extracted.txt")

    await api.uploadFile(server.id, "/", archive, createZip({ [extracted]: "e2e" }))
    await openFilesTab(page, server)

    await openFileActions(page, archive)

    const response = await clickAndWaitForApi(page, 'button[name="file-extract"]', FILES_API, "POST")
    expect(response.status()).toBe(204)
  })

  test("Should show validation warning on file move with empty destination via actions menu", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await openFileActions(page, file)
    await page.locator('button[name="file-move-popup"]').click()
    await page.locator('button[name="file-move"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on file move with empty destination via footer", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await selectFile(page, file)
    await page.locator('button[name="files-move-popup"]').click()
    await page.locator('button[name="file-move"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 204 on file move via actions menu", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")
    const dir = uniqueFileName("dir")

    await api.createFile(server.id, `/${file}`)
    await api.createFile(server.id, `/${dir}`, "directory")
    await openFilesTab(page, server)

    await openFileActions(page, file)
    await page.locator('button[name="file-move-popup"]').click()

    const response = await submitMove(page, `/${dir}`)
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file move via footer", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")
    const dir = uniqueFileName("dir")

    await api.createFile(server.id, `/${dir}`, "directory")
    await api.createFile(server.id, `/${dir}/${file}`)
    await openFilesTab(page, server)

    await openDirectory(page, dir)
    await selectFile(page, file)
    await page.locator('button[name="files-move-popup"]').click()

    const response = await submitMove(page, "/")
    expect(response.status()).toBe(204)
  })

  test("Should return 404 on file move with non-existing destination via actions menu", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await openFileActions(page, file)
    await page.locator('button[name="file-move-popup"]').click()

    const response = await submitMove(page, "/fictional_dir")
    expect(response.status()).toBe(404)
  })

  test("Should return 404 on file move with non-existing destination via footer", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await selectFile(page, file)
    await page.locator('button[name="files-move-popup"]').click()

    const response = await submitMove(page, "/fictional_dir")
    expect(response.status()).toBe(404)
  })

  test("Should show one row on file search", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await page.locator('input[name="search-input"]').fill(file)
    await page.locator('button[name="search-submit"]').click()

    const rows = page.locator("tbody tr")
    await expect(rows).toHaveCount(1)
    await expect(rows.first().locator("td", { hasText: file })).toBeVisible()
  })

  test("Should show empty table on file search with fictional name", async ({ page, server }) => {
    await openFilesTab(page, server)

    await page.locator('input[name="search-input"]').fill("fictional_file")
    await page.locator('button[name="search-submit"]').click()

    await expect(page.locator("tbody tr")).toHaveCount(0)
  })

  test("Should return 204 on file delete via actions menu", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await openFileActions(page, file)
    await page.locator('button[name="file-delete-popup"]').click()

    const response = await clickAndWaitForApi(page, 'button[name="confirm"]', FILES_API, "DELETE")
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file delete via footer", async ({ page, api, server }) => {
    const file = uniqueFileName("file.txt")

    await api.createFile(server.id, `/${file}`)
    await openFilesTab(page, server)

    await selectFile(page, file)
    await page.locator('button[name="files-delete-popup"]').click()

    const response = await clickAndWaitForApi(page, 'button[name="confirm"]', FILES_API, "DELETE")
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on directory delete", async ({ page, api, server }) => {
    const dir = uniqueFileName("dir")

    await api.createFile(server.id, `/${dir}`, "directory")
    await openFilesTab(page, server)

    await openFileActions(page, dir)
    await page.locator('button[name="file-delete-popup"]').click()

    const response = await clickAndWaitForApi(page, 'button[name="confirm"]', FILES_API, "DELETE")
    expect(response.status()).toBe(204)
  })
})

test.describe("Server page overview tab", () => {
  test("Should return 204 on server command", async ({ page, api, server }) => {
    await api.startServer(server.id)
    await openServerPage(page, server)

    const response = await sendServerCommand(page, "/help")
    expect(response.status()).toBe(204)
  })

  test("Should return 500 on server command with stopped server", async ({ page, api, server }) => {
    await api.stopServer(server.id)
    await openServerPage(page, server)

    const response = await sendServerCommand(page, "/help")
    expect(response.status()).toBe(500)
  })

  test("Should return 204 on server stop", async ({ page, api, server }) => {
    await api.startServer(server.id)
    await openServerPage(page, server)

    const response = await clickAndWaitForApi(
      page,
      'button[name="server-stop"]',
      /\/servers\/\d+\/stop(\?|$)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should show server start button on server stop", async ({ page, api, server }) => {
    await api.startServer(server.id)
    await openServerPage(page, server)

    await clickAndWaitForApi(
      page,
      'button[name="server-stop"]',
      /\/servers\/\d+\/stop(\?|$)/,
      "POST",
    )

    await expect(page.locator('button[name="server-start"]')).toBeVisible()
    await expect(page.locator('button[name="server-stop"]')).toHaveCount(0)
  })

  test("Should return 204 on server start", async ({ page, api, server }) => {
    await api.stopServer(server.id)
    await openServerPage(page, server)

    const response = await clickAndWaitForApi(
      page,
      'button[name="server-start"]',
      /\/servers\/\d+\/start(\?|$)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on server restart", async ({ page, api, server }) => {
    await api.startServer(server.id)
    await openServerPage(page, server)

    const response = await clickAndWaitForApi(
      page,
      'button[name="server-restart"]',
      /\/servers\/\d+\/restart(\?|$)/,
      "POST",
    )
    expect(response.status()).toBe(204)
  })
})
