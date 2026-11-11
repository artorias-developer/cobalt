/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { randomBytes } from "node:crypto"
import {
  test as base,
  expect,
  type APIRequestContext,
  type APIResponse,
  type Browser,
  type Page,
  type TestInfo,
} from "@playwright/test"

const API = "/api/v1"

/** Game, loader and version used for every test server (fast to install). */
const TEST_SERVER = {
  gameName: "rim_world",
  loaderName: "together",
}

/** Session saved by auth.setup.ts and shared by every authenticated test. */
const STORAGE_STATE = ".auth/session.json"

/** Maximum time to wait for a test server installation. */
const SERVER_INSTALL_TIMEOUT = 120_000

export const TEST_USER = {
  login: process.env.COBALT_LOGIN ?? "admin",
  password: process.env.COBALT_PASSWORD ?? "admin",
}

export interface RoleData {
  id: number
  name: string
}

export interface UserData {
  id: number
  login: string
  password: string
}

export interface ServerData {
  id: number
  name: string
  gameName: string
}

type EntityKind = "roles" | "users" | "servers"

/**
 * Generates a unique entity name so parallel tests never collide.
 *
 * Parameters:
 * - kind: Short entity kind used in the name (e.g. "role", "user").
 *
 * Returns:
 * - string: name in the "e2e_test_<kind>_<random>" format (at most 22 characters).
 */
export function uniqueName(kind: string): string {
  return `e2e_test_${kind}_${randomBytes(4).toString("hex")}`
}

/**
 * Asserts that an API response is successful and returns its JSON body.
 *
 * Parameters:
 * - response: Playwright API response.
 * - action: Human readable action name for the error message.
 *
 * Returns:
 * - Promise<any>: parsed JSON body, or null for empty responses.
 */
async function ensureOk(response: APIResponse, action: string): Promise<any> {
  if (!response.ok()) {
    throw new Error(`${action} failed: ${response.status()} ${await response.text()}`)
  }

  const text = await response.text()
  return text ? JSON.parse(text) : null
}

/**
 * Thin client over the Cobalt HTTP API used to prepare and clean up test data.
 * Every entity created or tracked through it is removed when the test ends.
 */
export class Api {
  private readonly created: Record<EntityKind, number[]> = { roles: [], users: [], servers: [] }
  private readonly tracked: Record<EntityKind, string[]> = { roles: [], users: [], servers: [] }

  constructor(private readonly request: APIRequestContext) {}

  /**
   * Creates a role.
   *
   * Parameters:
   * - name: Role name (unique name by default).
   * - permissions: Role permissions.
   *
   * Returns:
   * - Promise<RoleData>.
   */
  async createRole(name = uniqueName("role"), permissions: string[] = []): Promise<RoleData> {
    const body = await ensureOk(
      await this.request.post(`${API}/roles/`, { data: { name, permissions } }),
      "Role create",
    )
    this.created.roles.push(body.id)
    return { id: body.id, name: body.name }
  }

  /**
   * Creates a user. A new empty role is created when no role id is given.
   *
   * Parameters:
   * - login: User login (unique login by default).
   * - roleId: Role id to assign.
   * - password: User password.
   *
   * Returns:
   * - Promise<UserData>.
   */
  async createUser(
    login = uniqueName("user"),
    roleId?: number,
    password = "password",
  ): Promise<UserData> {
    const role_id = roleId ?? (await this.createRole()).id
    const body = await ensureOk(
      await this.request.post(`${API}/users/`, { data: { login, password, role_id } }),
      "User create",
    )
    this.created.users.push(body.id)
    return { id: body.id, login: body.login, password }
  }

  /**
   * Creates a test server and waits until it is installed and running.
   *
   * Parameters:
   * - name: Server name (unique name by default).
   *
   * Returns:
   * - Promise<ServerData>.
   */
  async createServer(name = uniqueName("server")): Promise<ServerData> {
    const testInfo = currentTestInfo()
    testInfo?.setTimeout(testInfo.timeout + SERVER_INSTALL_TIMEOUT)

    const games = await ensureOk(await this.request.get(`${API}/games/`), "Games fetch")
    const game = games.games.find((g: any) => g.name === TEST_SERVER.gameName)
    const loader = game.loaders.find((l: any) => l.name === TEST_SERVER.loaderName)

    const body = await ensureOk(
      await this.request.post(`${API}/servers/`, {
        data: { name, game_id: game.id, loader_id: loader.id, version: loader.versions[0] },
      }),
      "Server create",
    )
    this.created.servers.push(body.id)

    await expect.poll(
      async () => (await ensureOk(await this.request.get(`${API}/servers/${body.id}`), "Server fetch")).state,
      { timeout: SERVER_INSTALL_TIMEOUT, intervals: [500, 1_000] },
    ).toBe("installed")

    await this.waitForRunning(body.id, true)

    return { id: body.id, name: body.name, gameName: game.name }
  }

  /**
   * Waits until the server running status equals the expected value.
   *
   * Parameters:
   * - serverId: Server id.
   * - running: Expected running status.
   *
   * Returns:
   * - Promise<void>.
   */
  async waitForRunning(serverId: number, running: boolean): Promise<void> {
    await expect.poll(
      async () => (await ensureOk(await this.request.get(`${API}/servers/${serverId}/status`), "Server status")).running,
      { timeout: 60_000, intervals: [500, 1_000] },
    ).toBe(running)
  }

  /**
   * Stops a server (if it is running) and waits until it is no longer running.
   *
   * Parameters:
   * - serverId: Server id.
   *
   * Returns:
   * - Promise<void>.
   */
  async stopServer(serverId: number): Promise<void> {
    if (!(await this.isRunning(serverId))) return

    await ensureOk(await this.request.post(`${API}/servers/${serverId}/stop`), "Server stop")
    await this.waitForRunning(serverId, false)
  }

  /**
   * Starts a server (if it is stopped) and waits until it is running.
   *
   * Parameters:
   * - serverId: Server id.
   *
   * Returns:
   * - Promise<void>.
   */
  async startServer(serverId: number): Promise<void> {
    if (await this.isRunning(serverId)) return

    await ensureOk(await this.request.post(`${API}/servers/${serverId}/start`), "Server start")
    await this.waitForRunning(serverId, true)
  }

  /**
   * Returns the current server running status.
   *
   * Parameters:
   * - serverId: Server id.
   *
   * Returns:
   * - Promise<boolean>.
   */
  private async isRunning(serverId: number): Promise<boolean> {
    return (await ensureOk(await this.request.get(`${API}/servers/${serverId}/status`), "Server status")).running
  }

  /**
   * Creates a file or directory on a server.
   *
   * Parameters:
   * - serverId: Server id.
   * - path: Absolute path of the entry (e.g. "/dir/file.txt").
   * - type: "file" | "directory".
   *
   * Returns:
   * - Promise<void>.
   */
  async createFile(serverId: number, path: string, type: "file" | "directory" = "file"): Promise<void> {
    await ensureOk(
      await this.request.post(`${API}/servers/${serverId}/files/`, { data: { path, type } }),
      "File create",
    )
  }

  /**
   * Uploads a file to a server directory.
   *
   * Parameters:
   * - serverId: Server id.
   * - directory: Destination directory path.
   * - name: File name.
   * - buffer: File content.
   *
   * Returns:
   * - Promise<void>.
   */
  async uploadFile(serverId: number, directory: string, name: string, buffer: Buffer): Promise<void> {
    await ensureOk(
      await this.request.post(`${API}/servers/${serverId}/files/upload`, {
        params: { path: directory },
        multipart: { files: { name, mimeType: "application/octet-stream", buffer } },
      }),
      "File upload",
    )
  }

  /**
   * Registers an entity created through the UI so it is removed after the test.
   *
   * Parameters:
   * - kind: Entity kind.
   * - name: Role name, user login or server name.
   *
   * Returns:
   * - void.
   */
  track(kind: EntityKind, name: string): void {
    this.tracked[kind].push(name)
  }

  /**
   * Removes every entity created or tracked during the test.
   * Users go first, because roles that are still assigned cannot be deleted.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>.
   */
  async cleanup(): Promise<void> {
    for (const kind of ["users", "servers", "roles"] as const) {
      const ids = new Set(this.created[kind])

      for (const name of this.tracked[kind]) {
        for (const id of await this.findIds(kind, name)) ids.add(id)
      }

      for (const id of ids) {
        if (kind === "servers") {
          await this.deleteServer(id)
        } else {
          await this.request.delete(`${API}/${kind}/${id}`)
        }
      }
    }
  }

  /**
   * Deletes a server. A server that is still being installed cannot be
   * deleted, so its installation is canceled and the delete is retried.
   *
   * Parameters:
   * - serverId: Server id.
   *
   * Returns:
   * - Promise<void>.
   */
  private async deleteServer(serverId: number): Promise<void> {
    const deadline = Date.now() + 60_000

    while (Date.now() < deadline) {
      const response = await this.request.delete(`${API}/servers/${serverId}`)
      if (response.status() !== 409) return

      await this.request.post(`${API}/servers/${serverId}/cancel`)
      await new Promise((resolve) => setTimeout(resolve, 1_000))
    }
  }

  /**
   * Removes every test entity ("e2e_test_" prefix) left on the instance,
   * including servers shared by workers.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>.
   */
  async cleanupAll(): Promise<void> {
    for (const kind of ["users", "servers", "roles"] as const) {
      const ids: number[] = []

      for (let page = 1; ; page++) {
        const response = await this.request.get(`${API}/${kind}/`, {
          params: { search: "e2e_test_", limit: 100, page },
        })
        if (response.status() === 404) break

        const body = await ensureOk(response, `Test ${kind} fetch`)
        for (const item of body[kind] as any[]) {
          if ((item.name ?? item.login).startsWith("e2e_test_")) ids.push(item.id)
        }
        if (page >= body.pages) break
      }

      for (const id of ids) {
        if (kind === "servers") {
          await this.deleteServer(id)
        } else {
          await this.request.delete(`${API}/${kind}/${id}`)
        }
      }
    }
  }

  /**
   * Finds entity ids by exact name or login.
   *
   * Parameters:
   * - kind: Entity kind.
   * - name: Role name, user login or server name.
   *
   * Returns:
   * - Promise<number[]>.
   */
  private async findIds(kind: EntityKind, name: string): Promise<number[]> {
    const response = await this.request.get(`${API}/${kind}/`, { params: { search: name, limit: 100 } })
    if (!response.ok()) return []

    const body = await response.json()
    return (body[kind] as any[])
      .filter((item) => (item.name ?? item.login) === name)
      .map((item) => item.id)
  }
}

/**
 * Opens a new page in a fresh browser context signed in as the given user.
 * The session is independent of the shared storage state.
 *
 * Parameters:
 * - browser: Playwright browser instance.
 * - login: User login.
 * - password: User password.
 *
 * Returns:
 * - Promise<Page>: signed in page; its context is closed by the caller.
 */
export async function newSignedInPage(browser: Browser, login: string, password: string): Promise<Page> {
  const context = await browser.newContext({
    baseURL: process.env.COBALT_URL,
    ignoreHTTPSErrors: true,
    storageState: { cookies: [], origins: [] },
  })

  await ensureOk(
    await context.request.post(`${API}/auth/login`, { data: { login, password } }),
    "Sign in",
  )

  return context.newPage()
}

/**
 * Returns the info of the running test, or null outside of a test
 * (e.g. during worker fixture setup).
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - TestInfo | null.
 */
function currentTestInfo(): TestInfo | null {
  try {
    return base.info()
  } catch {
    return null
  }
}

/**
 * Generates a unique file or directory name for a test on a shared server.
 *
 * Parameters:
 * - name: Base name, optionally with an extension (e.g. "file.txt").
 *
 * Returns:
 * - string: name in the "e2e_test_<name>_<random>[.ext]" format.
 */
export function uniqueFileName(name: string): string {
  const dot = name.lastIndexOf(".")
  const stem = dot > 0 ? name.slice(0, dot) : name
  const extension = dot > 0 ? name.slice(dot) : ""
  return `${uniqueName(stem)}${extension}`
}

type TestFixtures = { api: Api, role: RoleData, user: UserData, server: ServerData }
type WorkerFixtures = { sharedServer: ServerData }

export const test = base.extend<TestFixtures, WorkerFixtures>({
  api: async ({ request }, use) => {
    const api = new Api(request)
    await use(api)
    await api.cleanup()
  },
  role: async ({ api }, use) => {
    await use(await api.createRole())
  },
  user: async ({ api }, use) => {
    await use(await api.createUser())
  },
  sharedServer: [async ({ playwright }, use) => {
    const request = await playwright.request.newContext({
      baseURL: process.env.COBALT_URL,
      ignoreHTTPSErrors: true,
      storageState: STORAGE_STATE,
    })
    const api = new Api(request)

    await use(await api.createServer())

    await api.cleanup()
    await request.dispose()
  }, { scope: "worker", timeout: SERVER_INSTALL_TIMEOUT + 60_000 }],
  server: async ({ sharedServer }, use) => {
    await use(sharedServer)
  },
})

export { expect }
