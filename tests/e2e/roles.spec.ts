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
 * Creates a role through the role-create popup.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: Name of the role to create.
 * - withPermissions: Whether to select the first permissions group.
 *
 * Returns:
 * - Promise<Response | undefined>: the API response for the create request,
 *   or undefined when the name is empty and no request is sent.
 */
async function createRole(
  page: Page,
  name: string,
  withPermissions: boolean = false,
): Promise<Response | undefined> {
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

  if (withPermissions) {
    const group = page.locator(".permissions .group .title").first()
    await group.waitFor({ state: "visible" })
    await group.click()
  }

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

/**
 * Opens a role row action popup after narrowing the table down by search,
 * so the row is found regardless of pagination.
 *
 * Parameters:
 * - page: Playwright page instance.
 * - name: Role name.
 * - action: Row action button name (e.g. "role-edit-popup").
 *
 * Returns:
 * - Promise<void>.
 */
async function openRoleAction(page: Page, name: string, action: string): Promise<void> {
  await searchRole(page, name)

  const row = page.locator("tr").filter({
    has: page.locator("td:nth-child(2)", { hasText: name }),
  })
  const button = row.locator(`button[name="${action}"]`)
  await button.waitFor({ state: "visible" })
  await expect(button).toBeEnabled()
  await button.click()
}

test.describe("Roles page", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/roles")
  })

  test("Should show validation warning on role create with empty name", async ({ page }) => {
    await createRole(page, "")
    await expect(page.locator(".vue-notification.warn")).toBeVisible()
  })

  test("Should return 200 on role create", async ({ page, api }) => {
    const name = uniqueName("role")
    api.track("roles", name)

    const response = await createRole(page, name)
    expect(response!.status()).toBe(200)
  })

  test("Should return 200 on role create with permissions", async ({ page, api }) => {
    const name = uniqueName("role")
    api.track("roles", name)

    const response = await createRole(page, name, true)
    expect(response!.status()).toBe(200)
    expect((await response!.json()).permissions.length).toBeGreaterThan(0)
  })

  test("Should return 409 on role create with existing name", async ({ page, role }) => {
    const response = await createRole(page, role.name)
    expect(response!.status()).toBe(409)
  })

  test("Should return 200 on role search", async ({ page, role }) => {
    const response = await searchRole(page, role.name)
    expect(response.status()).toBe(200)
  })

  test("Should return 404 on role search with fictional name", async ({ page }) => {
    const response = await searchRole(page, "fictional_role")
    expect(response.status()).toBe(404)
  })

  test("Should return 200 on role search reset", async ({ page, role }) => {
    await searchRole(page, role.name)

    const response = await clickAndWaitForApi(
      page,
      'button[name="search-reset"]',
      /roles/,
      "GET",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 200 on role update", async ({ page, role }) => {
    await openRoleAction(page, role.name, "role-edit-popup")

    const nameInput = page.locator('input[name="role-name"]')
    await nameInput.waitFor({ state: "visible" })
    await nameInput.fill(`${role.name}_updated`)

    const response = await clickAndWaitForApi(
      page,
      'button[name="role-update"]',
      /roles/,
      "PATCH",
    )
    expect(response.status()).toBe(200)
  })

  test("Should return 204 on role delete", async ({ page, role }) => {
    await openRoleAction(page, role.name, "role-delete-popup")

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /roles/,
      "DELETE",
    )
    expect(response.status()).toBe(204)
  })

  test("Should return 409 on role delete with assigned users", async ({ page, api, role }) => {
    await api.createUser(undefined, role.id)
    await openRoleAction(page, role.name, "role-delete-popup")

    const response = await clickAndWaitForApi(
      page,
      'button[name="confirm"]',
      /roles/,
      "DELETE",
    )
    expect(response.status()).toBe(409)
  })
})
