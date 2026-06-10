/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, type Page, type Response } from "@playwright/test"

async function createRole(page: Page, name: string): Promise<Response> {
  await page.locator('button[name="role-create-popup"]').click()
  await page.locator('input[name="role-name"]').fill(name)
  const [response] = await Promise.all([
    page.waitForResponse((resp) =>
      resp.url().includes("roles") && resp.request().method() === "POST"
    ),
    page.locator('button[name="role-create"]').click(),
  ])
  return response
}

async function searchRole(page: Page, name: string): Promise<Response> {
  await page.locator('input[name="search-input"]').fill(name)
  const [response] = await Promise.all([
    page.waitForResponse((resp) =>
      resp.url().includes("roles") && resp.request().method() === "GET"
    ),
    page.locator('button[name="search-submit"]').click(),
  ])
  return response
}

test.describe.configure({ mode: "serial" })

test.describe("Roles page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/roles", { waitUntil: "domcontentloaded" })
  })

  test("Should return 200 on role create", async ({ page }) => {
    const response = await createRole(page, "e2e_test_role")
    expect(response.status()).toBe(200)
  })

  test("Should return 409 on role create with existing name", async ({ page }) => {
    const response = await createRole(page, "e2e_test_role")
    expect(response.status()).toBe(409)
  })

  test("Should return 200 on role search", async ({ page }) => {
    const response = await searchRole(page, "e2e_test_role")
    expect(response.status()).toBe(200)
  })

  test("Should return 404 on fictional role search", async ({ page }) => {
    const response = await searchRole(page, "fictional_role")
    expect(response.status()).toBe(404)
  })

  test("Should return 200 on search reset", async ({ page }) => {
    await searchRole(page, "e2e_test_role")
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("roles") && resp.request().method() === "GET"
      ),
      page.locator('button[name="search-reset"]').click(),
    ])

    expect(response.status()).toBe(200)
  })

  test("Should return 200 on role update", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td:nth-child(2)", { hasText: "e2e_test_role" }),
    })
    await row.locator('button[name="role-edit-popup"]').click()
    await page.locator('input[name="role-name"]').fill("e2e_test_role_updated")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("roles") && resp.request().method() === "PATCH"
      ),
      page.locator('button[name="role-update"]').click(),
    ])

    expect(response.status()).toBe(200)
  })

  test("Should return 204 on role delete", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td:nth-child(2)", { hasText: "e2e_test_role_updated" }),
    })
    await row.locator('button[name="role-delete-popup"]').click()

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("roles") && resp.request().method() === "DELETE"
      ),
      page.locator('button[name="confirm"]').click(),
    ])

    expect(response.status()).toBe(204)
  })
})