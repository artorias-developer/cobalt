/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, type Page, type Response } from "@playwright/test"

async function createFile(
  page: Page,
  name: string,
  type: "File" | "Directory" = "File",
): Promise<Response> {
  await page.locator('button[name="file-create-popup"]').click()
  await page.locator('input[name="file-name"]').fill(name)
  await page.locator('div[aria-label="file-type"]').click()
  await page.locator(".select-dropdown .option").first().waitFor()
  await page.waitForTimeout(500)
  await page.locator(".select-dropdown .option").filter({ hasText: type }).click()

  const [response] = await Promise.all([
    page.waitForResponse((resp) =>
      resp.url().includes("files") && resp.request().method() === "POST"
    ),
    page.locator('button[name="file-create"]').click(),
  ])
  return response
}

async function getFileRow(page: Page, name: string) {
  return page.locator("tr").filter({
    has: page.locator("td", { hasText: name }),
  })
}

async function openFileActions(page: Page, name: string) {
  const row = await getFileRow(page, name)
  await row.locator(".actions-button .trigger").click()
}

async function selectFile(page: Page, name: string) {
  const row = await getFileRow(page, name)
  await row.locator("td .label-checkbox .checkbox").click()
}

test.describe.configure({ mode: "serial" })

test.describe("Server files", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/servers", { waitUntil: "domcontentloaded" })

    const row = page.locator("tr").filter({
      has: page.locator("td", { hasText: "e2e_test_server" }),
    })
    await row.locator('a[aria-label="server-settings"]').click()
    await page.locator('.tabs .nav button[name="files"]').click()
  })

  test("Should show warning on empty name at file create", async ({ page }) => {
    await page.locator('button[name="file-create-popup"]').click()
    await page.locator('button[name="file-create"]').click()

    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 204 on files and directory create", async ({ page }) => {
    const [response1] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      createFile(page, "e2e_test_file.txt"),
    ])
    expect(response1.status()).toBe(204)

    const [response2] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      createFile(page, "e2e_test_file2.txt"),
    ])
    expect(response2.status()).toBe(204)

    const [response3] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      createFile(page, "e2e_test_dir", "Directory"),
    ])
    expect(response3.status()).toBe(204)
  })

  test("Should return 409 on file create with existing name", async ({ page }) => {
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      createFile(page, "e2e_test_file.txt"),
    ])
    expect(response.status()).toBe(409)
  })

  test("Should return 200 on reload", async ({ page }) => {
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "GET"
      ),
      page.locator('button[name="file-reload-popup"]').click(),
    ])
    expect(response.status()).toBe(200)
  })

  test("Should return 204 on file open and save", async ({ page }) => {
    await openFileActions(page, "e2e_test_file.txt")
    await page.locator('button[name="file-open"]').click()

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "PUT"
      ),
      page.locator('button[name="file-save"]').click(),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file rename", async ({ page }) => {
    await openFileActions(page, "e2e_test_file.txt")
    await page.locator('button[name="file-rename-popup"]').click()
    await page.locator('input[name="file-name"]').fill("e2e_test_file_renamed.txt")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="file-rename"]').click(),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 409 on file rename to existing name", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="file-rename-popup"]').click()
    await page.locator('input[name="file-name"]').fill("e2e_test_file2.txt")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="file-rename"]').click(),
    ])
    expect(response.status()).toBe(409)
  })

  test("Should return 200 on file download via actions menu", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="file-download"]').click(),
    ])
    expect(response.status()).toBe(200)
  })

  test("Should return 200 on file download via footer", async ({ page }) => {
    await selectFile(page, "e2e_test_file_renamed.txt")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="files-download"]').click(),
    ])
    expect(response.status()).toBe(200)
  })

  test("Should return 204 on file duplicate via actions menu", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="file-duplicate"]').click(),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file duplicate via footer", async ({ page }) => {
    await selectFile(page, "e2e_test_file_renamed.txt")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="files-duplicate"]').click(),
    ])
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

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="file-move"]').click(),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file move via footer", async ({ page }) => {
    const dirRow = await getFileRow(page, "e2e_test_dir")
    await dirRow.locator("td").nth(1).click()

    await selectFile(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="files-move-popup"]').click()
    await page.locator('input[name="file-move-destination"]').fill("/")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="file-move"]').click(),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 404 on file move to non-existing directory via actions menu", async ({ page }) => {
    await openFileActions(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="file-move-popup"]').click()
    await page.locator('input[name="file-move-destination"]').fill("/fictional_dir")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="file-move"]').click(),
    ])
    expect(response.status()).toBe(404)
  })

  test("Should return 404 on file move to non-existing directory via footer", async ({ page }) => {
    await selectFile(page, "e2e_test_file_renamed.txt")
    await page.locator('button[name="files-move-popup"]').click()
    await page.locator('input[name="file-move-destination"]').fill("/fictional_dir")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "POST"
      ),
      page.locator('button[name="file-move"]').click(),
    ])
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

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "DELETE"
      ),
      page.locator('button[name="confirm"]').click(),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on file delete via footer", async ({ page }) => {
    await selectFile(page, "e2e_test_file2.txt")
    await page.locator('button[name="files-delete-popup"]').click()

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "DELETE"
      ),
      page.locator('button[name="confirm"]').click(),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on directory delete", async ({ page }) => {
    await openFileActions(page, "e2e_test_dir")
    await page.locator('button[name="file-delete-popup"]').click()

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("files") && resp.request().method() === "DELETE"
      ),
      page.locator('button[name="confirm"]').click(),
    ])
    expect(response.status()).toBe(204)
  })
})

test.describe("Server overview", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/servers", { waitUntil: "domcontentloaded" })

    const row = page.locator("tr").filter({
      has: page.locator("td", { hasText: "e2e_test_server" }),
    })
    await row.locator('a[aria-label="server-settings"]').click()
  })

  test("Should return 204 on console command", async ({ page }) => {
    await page.locator('input[name="server-console"]').fill("/help")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("servers") && resp.request().method() === "POST"
      ),
      page.locator('input[name="server-console"]').press("Enter"),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on server stop", async ({ page }) => {
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("servers") && resp.request().method() === "POST"
      ),
      page.locator('button[name="server-stop"]').click(),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 500 on console command when server is stopped", async ({ page }) => {
    await page.locator('input[name="server-console"]').fill("/help")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("servers") && resp.request().method() === "POST"
      ),
      page.locator('input[name="server-console"]').press("Enter"),
    ])
    expect(response.status()).toBe(500)
  })

  test("Should return 204 on server start", async ({ page }) => {
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("servers") && resp.request().method() === "POST"
      ),
      page.locator('button[name="server-start"]').click(),
    ])
    expect(response.status()).toBe(204)
  })

  test("Should return 204 on server restart", async ({ page }) => {
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("servers") && resp.request().method() === "POST"
      ),
      page.locator('button[name="server-restart"]').click(),
    ])
    expect(response.status()).toBe(204)
  })
})

test.describe("Servers page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/servers", { waitUntil: "domcontentloaded" })
  })

  test("Should return 204 on server delete", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td", { hasText: "e2e_test_server" }),
    })
    await row.locator('button[name="server-delete-popup"]').click()

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("servers") && resp.request().method() === "DELETE"
      ),
      page.locator('button[name="confirm"]').click(),
    ])
    expect(response.status()).toBe(204)
  })
})