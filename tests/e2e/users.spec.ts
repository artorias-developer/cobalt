/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect, type Page, type Response } from "@playwright/test"
import { gotoWithRetry, clickAndWaitForApi } from "./helpers/api.js"

/**
 * Creates a user through the user-create popup.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - login: Login of the user to create.
 * - password: Password for the user.
 * - selectRole: Whether to select a role option.
 *
 * Returns:
 * - Promise<Response | undefined>: the API response for the create request,
 *   or undefined when the flow stops early due to missing input.
 */
async function createUser(
  page: Page,
  login: string,
  password: string,
  selectRole: boolean = true,
): Promise<Response | undefined> {
  const createPopupButton = page.locator('button[name="user-create-popup"]')
  await createPopupButton.waitFor({ state: "visible" })
  await expect(createPopupButton).toBeEnabled()
  await createPopupButton.click()

  const createButton = page.locator('button[name="user-create"]')

  if (!login) {
    await createButton.waitFor({ state: "visible" })
    await expect(createButton).toBeEnabled()
    await createButton.click()
    return
  }

  const loginInput = page.locator('input[name="user-login"]')
  await loginInput.waitFor({ state: "visible" })
  await loginInput.fill(login)

  if (!password) {
    await createButton.waitFor({ state: "visible" })
    await expect(createButton).toBeEnabled()
    await createButton.click()
    return
  }

  const passwordInput = page.locator('input[name="user-password"]')
  await passwordInput.waitFor({ state: "visible" })
  await passwordInput.fill(password)

  if (!selectRole) {
    await createButton.waitFor({ state: "visible" })
    await expect(createButton).toBeEnabled()
    await createButton.click()
    return
  }

  const roleField = page.locator('div[aria-label="user-role"]')
  await roleField.waitFor({ state: "visible" })
  await roleField.click()

  const roleDropdown = page.locator(".select-dropdown")
  await roleDropdown.waitFor({ state: "visible" })

  const options = roleDropdown.locator(".option")
  await options.first().waitFor({ state: "visible" })

  const count = await options.count()
  for (let i = 0; i < count; i++) {
    const text = await options.nth(i).textContent()
    if (!text?.includes("e2e_test")) {
      await options.nth(i).click()
      break
    }
  }

  await roleDropdown.waitFor({ state: "hidden" })

  return clickAndWaitForApi(
    page,
    'button[name="user-create"]',
    /users/,
    "POST",
  )
}

/**
 * Searches for a user by login.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - login: Login to search for.
 *
 * Returns:
 * - Promise<Response>: the API response for the search request.
 */
async function searchUser(page: Page, login: string): Promise<Response> {
  const searchInput = page.locator('input[name="search-input"]')
  await searchInput.waitFor({ state: "visible" })
  await searchInput.fill(login)

  return clickAndWaitForApi(
    page,
    'button[name="search-submit"]',
    /users/,
    "GET",
  )
}

test.describe.configure({ mode: "serial" })

test.describe("Users page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/users")
  })

  test("Should show validation warning on empty login at user create", async ({ page }) => {
    await createUser(page, "", "password")
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on empty password at user create", async ({ page }) => {
    await createUser(page, "e2e_test_user_invalid", "")
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on unselected role at user create", async ({ page }) => {
    await createUser(page, "e2e_test_user_invalid", "password", false)
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 200 on user create", async ({ page }) => {
    const response = await createUser(page, "e2e_test_user", "password")
    expect(response!.status()).toBe(200)
  })

  test("Should return 409 on user create with existing login", async ({ page }) => {
    const response = await createUser(page, "e2e_test_user", "password")
    expect(response!.status()).toBe(409)
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

    const response = await clickAndWaitForApi(
      page,
      'button[name="search-reset"]',
      /users/,
      "GET",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 200 on user update", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td:nth-child(2)", { hasText: "e2e_test_user" }),
    })
    const editButton = row.locator('button[name="user-edit-popup"]')
    await editButton.waitFor({ state: "visible" })
    await expect(editButton).toBeEnabled()
    await editButton.click()

    const loginInput = page.locator('input[name="user-login"]')
    await loginInput.waitFor({ state: "visible" })
    await loginInput.fill("e2e_test_user_updated")

    const response = await clickAndWaitForApi(
      page,
      'button[name="user-update"]',
      /users/,
      "PATCH",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 204 on user delete", async ({ page }) => {
    const row = page.locator("tr").filter({
      has: page.locator("td:nth-child(2)", { hasText: "e2e_test_user_updated" }),
    })
    const deleteButton = row.locator('button[name="user-delete-popup"]')
    await deleteButton.waitFor({ state: "visible" })
    await expect(deleteButton).toBeEnabled()
    await deleteButton.click()

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /users/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })
})