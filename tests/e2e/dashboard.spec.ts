/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test, expect } from "@playwright/test"
import { gotoWithRetry, clickAndWaitForApi } from "./helpers/api.js"

test.describe("Dashboard page", () => {
  test("Should return 200 on disk metrics reload", async ({ page }) => {
    await gotoWithRetry(page, "/")

    const response = await clickAndWaitForApi(
      page,
      '.block.disk button[name="reload"]',
      /disk/,
      "GET",
    )
    expect(response.status()).toBe(200)
  })
})