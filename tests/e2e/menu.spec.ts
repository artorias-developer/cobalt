/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"
import { gotoWithRetry } from "./helpers/api.js"

test.describe("Menu", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRetry(page, "/")
  })

  test("Should open Dashboard page on menu item click", async ({ page }) => {
    const link = page.locator('.menu a[aria-label="dashboard"]')
    await link.waitFor({ state: "visible" })
    await expect(link).toBeEnabled()
    await link.click()

    await expect(page.locator(".page .metrics")).toBeVisible()
  })

  test("Should open Servers page on menu item click", async ({ page }) => {
    const link = page.locator('.menu a[aria-label="servers"]')
    await link.waitFor({ state: "visible" })
    await expect(link).toBeEnabled()
    await link.click()

    await expect(page.locator(".page .block.servers")).toBeVisible()
  })

  test("Should open Users page on menu item click", async ({ page }) => {
    const link = page.locator('.menu a[aria-label="users"]')
    await link.waitFor({ state: "visible" })
    await expect(link).toBeEnabled()
    await link.click()

    await expect(page.locator(".page .block.users")).toBeVisible()
  })

  test("Should open Roles page on menu item click", async ({ page }) => {
    const link = page.locator('.menu a[aria-label="roles"]')
    await link.waitFor({ state: "visible" })
    await expect(link).toBeEnabled()
    await link.click()

    await expect(page.locator(".page .block.roles")).toBeVisible()
  })

  test("Should open Settings page on menu item click", async ({ page }) => {
    const link = page.locator('.menu a[aria-label="settings"]')
    await link.waitFor({ state: "visible" })
    await expect(link).toBeEnabled()
    await link.click()

    await expect(page.locator(".page .block.settings")).toBeVisible()
  })

  test("Should open GitHub repository on menu item click", async ({ page }) => {
    const githubLink = page.locator(".menu .banners .github")
    await githubLink.waitFor({ state: "visible" })
    await expect(githubLink).toBeEnabled()

    const [newPage] = await Promise.all([
      page.waitForEvent("popup"),
      githubLink.click(),
    ])
    await newPage.waitForLoadState()

    await expect(newPage).toHaveURL(/github\.com/)
  })

  test("Should open Support popup on menu item click", async ({ page }) => {
    const walletButton = page.locator(".menu .banners .support .wallets button").first()
    await walletButton.waitFor({ state: "visible" })
    await expect(walletButton).toBeEnabled()
    await walletButton.click()

    await expect(page.locator(".wallet-popup")).toBeVisible()
  })

  test("Should open GitHub issues on menu item click", async ({ page }) => {
    const helpLink = page.locator('.menu a[aria-label="help"]')
    await helpLink.waitFor({ state: "visible" })
    await expect(helpLink).toBeEnabled()

    const [newPage] = await Promise.all([
      page.waitForEvent("popup"),
      helpLink.click(),
    ])
    await newPage.waitForLoadState()

    await expect(newPage).toHaveURL(/github\.com/)
  })
})