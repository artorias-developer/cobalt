/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import dotenv from "dotenv"
import { defineConfig, devices } from "@playwright/test"

import path from "node:path"
import {fileURLToPath} from "node:url"


const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

dotenv.config({ path: path.resolve(__dirname, ".env"), quiet: true })

const isCI = process.env.CI === "true" || process.env.CI === "1"

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: isCI,
  retries: isCI ? 2 : 0,
  workers: isCI ? 1 : 2,
  reporter: [
    ["list"],
    ["html", { open: "on-failure" }]
  ],
  use: {
    baseURL: process.env.COBALT_URL,
    ignoreHTTPSErrors: true,
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    trace: "retain-on-failure"
  },
  projects: [
    {
      name: "setup",
      testMatch: "**/auth.setup.ts",
      use: {
        ...devices["Desktop Firefox"],
      }
    },
    {
      name: "main",
      use: {
        ...devices["Desktop Firefox"],
        storageState: ".auth/session.json",
      },
      dependencies: ["setup"],
      testIgnore: ["**/logout.spec.ts", "**/servers.spec.ts", "**/server.spec.ts"]
    },
    {
      name: "servers",
      use: {
        ...devices["Desktop Firefox"],
        storageState: ".auth/session.json",
      },
      dependencies: ["main"],
      testMatch: "**/servers.spec.ts"
    },
    {
      name: "server",
      use: {
        ...devices["Desktop Firefox"],
        storageState: ".auth/session.json",
      },
      dependencies: ["servers"],
      testMatch: "**/server.spec.ts"
    },
    {
      name: "logout",
      use: {
        ...devices["Desktop Firefox"],
        storageState: ".auth/session.json",
      },
      dependencies: ["server"],
      testMatch: "**/logout.spec.ts"
    }
  ]
})