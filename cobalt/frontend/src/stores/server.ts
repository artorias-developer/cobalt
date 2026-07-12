// Copyright (C) 2026 Artorias
// Author: Artorias
// Repository: https://github.com/artorias-developer/cobalt
// SPDX-License-Identifier: AGPL-3.0-or-later

import { defineStore } from "pinia"
import { ref } from "vue"

import { type ServerEntity, ServerStateEnum, type ServerStatusEntity } from "@/types"

interface ServerState {
  server: ServerEntity | null
  status: ServerStatusEntity | null
  hostname: string | null
  loaderVersions: string[]
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
        hostname: null,
        loaderVersions: []
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
   * Returns the state of the server entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - ServerStateEnum | undefined.
   */
  function getState(serverId: number): ServerStateEnum | undefined {
    return ensure(serverId).server?.state
  }

  /**
   * Updates the state field of the server entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - state: ServerStateEnum - state value to set.
   *
   * Returns:
   * - void.
   */
  function setState(serverId: number, state: ServerStateEnum): void {
    const s = ensure(serverId)
    if (!s.server) return
    s.server = { ...s.server, state }
  }

  /**
   * Returns the version of the server entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - string | undefined.
   */
  function getVersion(serverId: number): string | undefined {
    return ensure(serverId).server?.version
  }

  /**
   * Updates the version field of the server entity for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - version: string - version value to set.
   *
   * Returns:
   * - void.
   */
  function setVersion(serverId: number, version: string): void {
    const state = ensure(serverId)
    if (!state.server) return
    state.server = { ...state.server, version }
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
   * Returns the loader versions list for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - string[].
   */
  function getLoaderVersions(serverId: number): string[] {
    return ensure(serverId).loaderVersions
  }

  /**
   * Sets the loader versions list for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - versions: string[] - loader versions to set.
   *
   * Returns:
   * - void.
   */
  function setLoaderVersions(serverId: number, versions: string[]): void {
    ensure(serverId).loaderVersions = versions
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
    getState,
    setState,
    getVersion,
    setVersion,
    setRunning,
    setPort,
    getHostname,
    setHostname,
    getLoaderVersions,
    setLoaderVersions,
    clear
  }
})