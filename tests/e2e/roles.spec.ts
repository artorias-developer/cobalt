/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, type Page, type Response } from "@playwright/test"
import { gotoWithRetry, clickAndWaitForApi } from "./helpers/api.js"

/**
 * Creates a role through the role-create popup.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: Name of the role to create.
 *
 * Returns:
 * - Promise<Response | undefined>: the API response for the create request,
 *   or undefined when the name is empty and no request is sent.
 */
async function createRole(page: Page, name: string): Promise<Response | undefined> {
  const createPopupButton = page.locator('button[name="role-create-popup"]')
  await createPopupButton.waitFor({ state: "visible" })
  await expect(createPopupButton).toBeEnabled()
  await createPopupButton.click()

  if (!name) {
    const createButton = page.locator('button[name="role-create"]')
    await createButton.waitFor({ state: "visible" })
    await expect(createButton).toBeEnabled()
    await createButton.click()
    return
  }

  const nameInput = page.locator('input[name="role-name"]')
  await nameInput.waitFor({ state: "visible" })
  await nameInput.fill(name)

  return clickAndWaitForApi(
    page,
    'button[name="role-create"]',
    /roles/,
    "POST",
  )
}

/**
 * Searches for a role by name.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: Role name to search for.
 *
 * Returns:
 * - Promise<Response>: the API response for the search request.
 */
async function searchRole(page: Page, name: string): Promise<Response> {
  const searchInput = page.locator('input[name="search-input"]')
  await searchInput.waitFor({ state: "visible" })
  await searchInput.fill(name)

  return clickAndWaitForApi(
    page,
    'button[name="search-submit"]',
    /roles/,
    "GET",
  )
}

test.describe.configure({ mode: "serial" })

test.describe("Roles page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/roles")
  })

  test("Should show validation warning on empty role name", async ({ page }) => {
    await createRole(page, "")
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 200 on role create", async ({ page }) => {
    const response = await createRole(page, "e2e_test_role")
    expect(response!.status()).toBe(200)
  })

  test("Should return 409 on role create with existing name", async ({ page }) => {
    const response = await createRole(page, "e2e_test_role")
    expect(response!.status()).toBe(409)
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

    const response = await clickAndWaitForApi(
      page,
      'button[name="search-reset"]',
      /roles/,
      "GET",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 200 on role update", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td:nth-child(2)", { hasText: "e2e_test_role" }),
    })
    const editButton = row.locator('button[name="role-edit-popup"]')
    await editButton.waitFor({ state: "visible" })
    await expect(editButton).toBeEnabled()
    await editButton.click()

    const nameInput = page.locator('input[name="role-name"]')
    await nameInput.waitFor({ state: "visible" })
    await nameInput.fill("e2e_test_role_updated")

    const response = await clickAndWaitForApi(
      page,
      'button[name="role-update"]',
      /roles/,
      "PATCH",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 204 on role delete", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td:nth-child(2)", { hasText: "e2e_test_role_updated" }),
    })
    const deleteButton = row.locator('button[name="role-delete-popup"]')
    await deleteButton.waitFor({ state: "visible" })
    await expect(deleteButton).toBeEnabled()
    await deleteButton.click()

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /roles/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })
})