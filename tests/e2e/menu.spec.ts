/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"

test.describe("Menu", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/', { waitUntil: "domcontentloaded" })
  })

  test("Should open Dashboard page on menu item click", async ({ page }) => {
    await page.locator('.menu a[aria-label="dashboard"]').click()

    await expect(page.locator(".page .metrics")).toBeVisible()
  })

  test("Should open Servers page on menu item click", async ({ page }) => {
    await page.locator('.menu a[aria-label="servers"]').click()

    await expect(page.locator(".page .block.servers")).toBeVisible()
  })

  test("Should open Users page on menu item click", async ({ page }) => {
    await page.locator('.menu a[aria-label="users"]').click()

    await expect(page.locator(".page .block.users")).toBeVisible()
  })

  test("Should open Roles page on menu item click", async ({ page }) => {
    await page.locator('.menu a[aria-label="roles"]').click()

    await expect(page.locator(".page .block.roles")).toBeVisible()
  })

  test("Should open Settings page on menu item click", async ({ page }) => {
    await page.locator('.menu a[aria-label="settings"]').click()

    await expect(page.locator(".page .block.settings")).toBeVisible()
  })

  test("Should open GitHub repository on menu item click", async ({ page }) => {
    const [newPage] = await Promise.all([
      page.waitForEvent("popup"),
      page.locator(".menu .banners .github").click(),
    ])
    await newPage.waitForLoadState()

    await expect(newPage).toHaveURL(/github\.com/)
  })

  test("Should open Support popup on menu item click", async ({ page }) => {
    await page.locator(".menu .banners .support .wallets button").first().click()

    await expect(page.locator(".wallet-popup")).toBeVisible()
  })

  test("Should open GitHub issues on menu item click", async ({ page }) => {
    const [newPage] = await Promise.all([
      page.waitForEvent("popup"),
      page.locator('.menu a[aria-label="help"]').click(),
    ])
    await newPage.waitForLoadState()

    await expect(newPage).toHaveURL(/github\.com/)
  })
})