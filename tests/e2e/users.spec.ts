/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, type Page, type Response } from "@playwright/test"

async function createUser(page: Page, login: string, password: string): Promise<Response> {
  await page.locator('button[name="user-create-popup"]').click()
  await page.locator('input[name="user-login"]').fill(login)
  await page.locator('input[name="user-password"]').fill(password)
  await page.locator('div[aria-label="user-role"]').click()
  await page.locator(".select-dropdown .option").first().waitFor()
  await page.waitForTimeout(500)
  const options = page.locator(".select-dropdown .option")
  const count = await options.count()
  for (let i = 0; i < count; i++) {
    const text = await options.nth(i).textContent()
    if (!text?.includes("e2e_test")) {
      await options.nth(i).click()
      break
    }
  }

  const [response] = await Promise.all([
    page.waitForResponse((resp) =>
      resp.url().includes("users") && resp.request().method() === "POST"
    ),
    page.locator('button[name="user-create"]').click(),
  ])
  return response
}

async function searchUser(page: Page, login: string): Promise<Response> {
  await page.locator('input[name="search-input"]').fill(login)
  const [response] = await Promise.all([
    page.waitForResponse((resp) =>
      resp.url().includes("users") && resp.request().method() === "GET"
    ),
    page.locator('button[name="search-submit"]').click(),
  ])
  return response
}

test.describe.configure({ mode: "serial" })

test.describe("Users page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/users")
  })

  test("Should return 200 on user create", async ({ page }) => {
    const response = await createUser(page, "e2e_test_user", "password")
    expect(response.status()).toBe(200)
  })

  test("Should return 409 on user create", async ({ page }) => {
    const response = await createUser(page, "e2e_test_user", "password")
    expect(response.status()).toBe(409)
  })

  test("Should return 200 on user search", async ({ page }) => {
    const response = await searchUser(page, "e2e_test_user")
    expect(response.status()).toBe(200)
  })

  test("Should return 404 on fictional user search", async ({ page }) => {
    const response = await searchUser(page, "fictional_user")
    expect(response.status()).toBe(404)
  })

  test("Should return 200 on search reset", async ({ page }) => {
    await searchUser(page, "e2e_test_user")
    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("users") && resp.request().method() === "GET"
      ),
      page.locator('button[name="search-reset"]').click(),
    ])

    expect(response.status()).toBe(200)
  })

  test("Should return 200 on user update", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td:nth-child(2)", { hasText: "e2e_test_user" }),
    })
    await row.locator('button[name="user-edit-popup"]').click()
    await page.locator('input[name="user-login"]').fill("e2e_test_user_updated")

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("users") && resp.request().method() === "PATCH"
      ),
      page.locator('button[name="user-update"]').click(),
    ])

    expect(response.status()).toBe(200)
  })

  test("Should return 204 on user delete", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td:nth-child(2)", { hasText: "e2e_test_user_updated" }),
    })
    await row.locator('button[name="user-delete-popup"]').click()

    const [response] = await Promise.all([
      page.waitForResponse((resp) =>
        resp.url().includes("users") && resp.request().method() === "DELETE"
      ),
      page.locator('button[name="confirm"]').click(),
    ])

    expect(response.status()).toBe(204)
  })
})