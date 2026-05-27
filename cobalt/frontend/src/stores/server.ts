// Copyright (C) 2026 ArtoriasCode
// Author: ArtoriasCode
// Repository: https://github.com/ArtoriasCode/cobalt
// SPDX-License-Identifier: AGPL-3.0-or-later

import { defineStore } from "pinia"
import { ref } from "vue"

import type { ServerEntity, ServerStatusEntity } from "@/types"

interface ServerState {
  server: ServerEntity | null
  status: ServerStatusEntity | null
  hostname: string | null
}

export const useServerStore = defineStore("server", () => {
  const servers = ref<Map<number, ServerState>>(new Map())

  /**
   * Returns existing server state or initializes a new one with defaults.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - ServerState.
   */
  function ensure(serverId: number): ServerState {
    if (!servers.value.has(serverId)) {
      servers.value.set(serverId, {
        server: null,
        status: null,
        hostname: null
      })
    }
    return servers.value.get(serverId)!
  }

  /**
   * Returns the server entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - ServerEntity | null.
   */
  function getServer(serverId: number): ServerEntity | null {
    return ensure(serverId).server
  }

  /**
   * Sets the full server entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - server: ServerEntity | null - server entity to set.
   *
   * Returns:
   * - void.
   */
  function setServer(serverId: number, server: ServerEntity | null): void {
    ensure(serverId).server = server
  }

  /**
   * Returns the status entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - ServerStatusEntity | null.
   */
  function getStatus(serverId: number): ServerStatusEntity | null {
    return ensure(serverId).status
  }

  /**
   * Sets the full status entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - status: ServerStatusEntity | null - status entity to set.
   *
   * Returns:
   * - void.
   */
  function setStatus(serverId: number, status: ServerStatusEntity | null): void {
    ensure(serverId).status = status
  }

  /**
   * Updates the running field of the status entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - running: boolean - running state to set.
   *
   * Returns:
   * - void.
   */
  function setRunning(serverId: number, running: boolean): void {
    const state = ensure(serverId)
    if (!state.status) return
    state.status = { ...state.status, running }
  }

  /**
   * Updates the port field of the status entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - port: number | null - port value to set.
   *
   * Returns:
   * - void.
   */
  function setPort(serverId: number, port: number | null): void {
    const state = ensure(serverId)
    if (!state.status) return
    state.status = { ...state.status, port }
  }

  /**
   * Returns the hostname for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - string | null.
   */
  function getHostname(serverId: number): string | null {
    return ensure(serverId).hostname
  }

  /**
   * Sets the hostname for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - hostname: string - hostname value to set.
   *
   * Returns:
   * - void.
   */
  function setHostname(serverId: number, hostname: string): void {
    ensure(serverId).hostname = hostname
  }

  /**
   * Removes all state for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - void.
   */
  function clear(serverId: number): void {
    servers.value.delete(serverId)
  }

  return {
    servers,
    getServer,
    setServer,
    getStatus,
    setStatus,
    setRunning,
    setPort,
    getHostname,
    setHostname,
    clear
  }
})