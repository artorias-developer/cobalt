//  Copyright (C) 2026 Artorias
//  Author: Artorias
//  Repository: https://github.com/artorias-developer/cobalt
//  SPDX-License-Identifier: AGPL-3.0-or-later

import { defineStore } from "pinia"
import { ref } from "vue"

const MAX_HISTORY = 20
const STORAGE_KEY_PREFIX = "console-history"

interface ConsoleState {
  history: string[]
  index: number
  draft: string
}

export const useServerConsoleStore = defineStore("serverConsole", () => {
  const consoles = ref<Map<number, ConsoleState>>(new Map())

  /**
   * Returns the localStorage key for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - string.
   */
  function storageKey(serverId: number): string {
    return `${STORAGE_KEY_PREFIX}:${serverId}`
  }

  /**
   * Returns existing console state or initializes a new one, loading history from localStorage.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - ConsoleState.
   */
  function ensure(serverId: number): ConsoleState {
    if (!consoles.value.has(serverId)) {
      let history: string[] = []

      try {
        const raw = localStorage.getItem(storageKey(serverId))
        history = raw ? JSON.parse(raw) : []
      } catch {
        history = []
      }

      consoles.value.set(serverId, {
        history,
        index: -1,
        draft: ""
      })
    }
    return consoles.value.get(serverId)!
  }

  /**
   * Persists the history array for a given server ID to localStorage.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - void.
   */
  function persist(serverId: number): void {
    try {
      localStorage.setItem(storageKey(serverId), JSON.stringify(ensure(serverId).history))
    } catch {
      // Ignore storage errors (quota exceeded, disabled, etc.)
    }
  }

  /**
   * Returns the command history list for a given server ID.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - string[].
   */
  function getHistory(serverId: number): string[] {
    return ensure(serverId).history
  }

  /**
   * Adds a command to history, skipping if identical to the last entry.
   * Trims to MAX_HISTORY most recent entries and persists to localStorage.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - value: string - command to add.
   *
   * Returns:
   * - void.
   */
  function push(serverId: number, value: string): void {
    const trimmed = value.trim()
    if (!trimmed) return

    const state = ensure(serverId)
    const last = state.history[state.history.length - 1]
    if (last === trimmed) return

    state.history.push(trimmed)

    if (state.history.length > MAX_HISTORY) {
      state.history = state.history.slice(-MAX_HISTORY)
    }

    persist(serverId)
  }

  /**
   * Navigates to the previous (older) command in history.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   * - currentValue: string - current input value, saved as draft on first navigation.
   *
   * Returns:
   * - string | null: The command to display, or null if history is empty.
   */
  function navigateUp(serverId: number, currentValue: string): string | null {
    const state = ensure(serverId)
    if (state.history.length === 0) return null

    if (state.index === -1) {
      state.draft = currentValue
      state.index = state.history.length - 1
    } else if (state.index > 0) {
      state.index -= 1
    }

    return state.history[state.index] ?? null
  }

  /**
   * Navigates to the next (newer) command in history, or back to the draft.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - string | null: The command to display, or null if not currently navigating.
   */
  function navigateDown(serverId: number): string | null {
    const state = ensure(serverId)
    if (state.index === -1) return null

    if (state.index < state.history.length - 1) {
      state.index += 1
      return state.history[state.index] ?? null
    }

    state.index = -1
    return state.draft
  }

  /**
   * Resets the navigation index and draft for a given server ID after a command is executed.
   *
   * Parameters:
   * - serverId: number - unique identifier of the server.
   *
   * Returns:
   * - void.
   */
  function resetNavigation(serverId: number): void {
    const state = ensure(serverId)
    state.index = -1
    state.draft = ""
  }

  return {
    consoles,
    getHistory,
    push,
    navigateUp,
    navigateDown,
    resetNavigation
  }
})