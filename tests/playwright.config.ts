/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { defineConfig, devices } from "@playwright/test"

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 2,
  reporter: "html",
  use: {
    baseURL: process.env.BASE_URL ?? "https://127.0.0.1",
    ignoreHTTPSErrors: true,
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    trace: "retain-on-failure"
  },
  projects: [
    {
      name: "setup",
      testMatch: "**/auth.setup.ts"
    },
    {
      name: "main",
      use: {
        ...devices["Desktop Chrome"],
        storageState: ".auth/session.json",
      },
      dependencies: ["setup"],
      testIgnore: ["**/logout.spec.ts", "**/servers.spec.ts", "**/server.spec.ts"]
    },
    {
      name: "servers",
      use: {
        ...devices["Desktop Chrome"],
        storageState: ".auth/session.json",
      },
      dependencies: ["main"],
      testMatch: "**/servers.spec.ts"
    },
    {
      name: "server",
      use: {
        ...devices["Desktop Chrome"],
        storageState: ".auth/session.json",
      },
      dependencies: ["servers"],
      testMatch: "**/server.spec.ts"
    },
    {
      name: "logout",
      use: {
        ...devices["Desktop Chrome"],
        storageState: ".auth/session.json",
      },
      dependencies: ["server"],
      testMatch: "**/logout.spec.ts"
    }
  ]
})