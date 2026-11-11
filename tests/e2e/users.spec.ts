/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { Page, Response } from "@playwright/test"
import { test, expect, uniqueName } from "./helpers/fixtures.js"
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

/**
 * Opens a user row action popup after narrowing the table down by search,
 * so the row is found regardless of pagination.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - login: User login.
 * - action: Row action button name (e.g. "user-edit-popup").
 *
 * Returns:
 * - Promise<void>.
 */
async function openUserAction(page: Page, login: string, action: string): Promise<void> {
  await searchUser(page, login)

  const row = page.locator("tr").filter({
    has: page.locator("td:nth-child(2)", { hasText: login }),
  })
  const button = row.locator(`button[name="${action}"]`)
  await button.waitFor({ state: "visible" })
  await expect(button).toBeEnabled()
  await button.click()
}

/**
 * Changes the login in the opened user-edit popup and submits it.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - login: New login.
 *
 * Returns:
 * - Promise<Response>: the API response for the update request.
 */
async function updateUserLogin(page: Page, login: string): Promise<Response> {
  const loginInput = page.locator('input[name="user-login"]')
  await loginInput.waitFor({ state: "visible" })
  await loginInput.fill(login)

  return clickAndWaitForApi(
    page,
    'button[name="user-update"]',
    /users/,
    "PATCH",
  )
}

test.describe("Users page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/users")
  })

  test("Should show validation warning on user create with empty login", async ({ page }) => {
    await createUser(page, "", "password")
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on user create with empty password", async ({ page }) => {
    await createUser(page, uniqueName("user"), "")
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should show validation warning on user create with unselected role", async ({ page }) => {
    await createUser(page, uniqueName("user"), "password", false)
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 200 on user create", async ({ page, api }) => {
    const login = uniqueName("user")
    api.track("users", login)

    const response = await createUser(page, login, "password")
    expect(response!.status()).toBe(200)
  })

  test("Should return 409 on user create with existing login", async ({ page, user }) => {
    const response = await createUser(page, user.login, "password")
    expect(response!.status()).toBe(409)
  })

  test("Should return 200 on user search", async ({ page, user }) => {
    const response = await searchUser(page, user.login)
    expect(response.status()).toBe(200)
  })

  test("Should return 404 on user search with fictional login", async ({ page }) => {
    const response = await searchUser(page, "fictional_user")
    expect(response.status()).toBe(404)
  })

  test("Should return 200 on user search reset", async ({ page, user }) => {
    await searchUser(page, user.login)

    const response = await clickAndWaitForApi(
      page,
      'button[name="search-reset"]',
      /users/,
      "GET",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 200 on user update", async ({ page, user }) => {
    await openUserAction(page, user.login, "user-edit-popup")

    const response = await updateUserLogin(page, `${user.login}_updated`)
    expect(response.status()).toBe(200)
  })

  test("Should return 409 on user update with existing login", async ({ page, api, user }) => {
    const other = await api.createUser()
    await openUserAction(page, user.login, "user-edit-popup")

    const response = await updateUserLogin(page, other.login)
    expect(response.status()).toBe(409)
  })

  test("Should return 204 on user delete", async ({ page, user }) => {
    await openUserAction(page, user.login, "user-delete-popup")

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /users/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })
})