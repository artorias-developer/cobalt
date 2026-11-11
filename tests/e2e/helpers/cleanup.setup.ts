/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { test as cleanup } from "@playwright/test"
import { Api } from "./fixtures.js"

cleanup("Remove test data", async ({ request }) => {
  await new Api(request).cleanupAll()
})
