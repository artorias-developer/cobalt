// Copyright (C) 2026 ArtoriasCode
// Author: ArtoriasCode
// Repository: https://github.com/ArtoriasCode/cobalt
// SPDX-License-Identifier: AGPL-3.0-or-later

import { defineStore } from "pinia"
import { ref } from "vue"

import type { SortState, TableState } from "@/types"

export const useTableStore = defineStore("table", () => {
  const tables = ref<Map<string, TableState>>(new Map())

  /**
   * Returns existing table state or initializes a new one with defaults.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   *
   * Returns:
   * - TableState.
   */
  function ensure(tableId: string): TableState {
    if (!tables.value.has(tableId)) {
      tables.value.set(tableId, {
        selected: new Set(),
        selectionVersion: 0,
        sort: null,
        page: 1,
        search: ""
      })
    }

    return tables.value.get(tableId)!
  }

  /**
   * Returns the set of selected row ids for a table.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   *
   * Returns:
   * - Set<string | number>.
   */
  function getSelected(tableId: string): Set<string | number> {
    return ensure(tableId).selected
  }

  /**
   * Returns current selection version (increments on every selection change).
   * Use as a reactive dependency to track Set mutations.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   *
   * Returns:
   * - number.
   */
  function getSelectionVersion(tableId: string): number {
    return ensure(tableId).selectionVersion
  }

  /**
   * Checks whether a specific row is selected.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   * - id: string | number - unique identifier of the row.
   *
   * Returns:
   * - boolean.
   */
  function isSelected(tableId: string, id: string | number): boolean {
    return ensure(tableId).selected.has(id)
  }

  /**
   * Checks whether all provided rows are selected.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   * - ids: Array<string | number> - list of row identifiers to check.
   *
   * Returns:
   * - boolean.
   */
  function isAllSelected(tableId: string, ids: Array<string | number>): boolean {
    if (ids.length === 0) return false
    const selected = ensure(tableId).selected

    return ids.every(id => selected.has(id))
  }

  /**
   * Toggles selection state for a single row.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   * - id: string | number - unique identifier of the row to toggle.
   *
   * Returns:
   * - void.
   */
  function toggleItemSelection(tableId: string, id: string | number): void {
    const state = ensure(tableId)
    state.selected.has(id) ? state.selected.delete(id) : state.selected.add(id)
    state.selectionVersion++
  }

  /**
   * Toggles selection state for all provided rows.
   * If all are selected, deselects all. Otherwise, selects all.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   * - ids: Array<string | number> - list of row identifiers to toggle.
   *
   * Returns:
   * - void.
   */
  function toggleAllSelection(tableId: string, ids: Array<string | number>): void {
    const state = ensure(tableId)
    const allSelected = ids.every(id => state.selected.has(id))
    allSelected
      ? ids.forEach(id => state.selected.delete(id))
      : ids.forEach(id => state.selected.add(id))
    state.selectionVersion++
  }

  /**
   * Clears all selected rows for a table.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   *
   * Returns:
   * - void.
   */
  function clearSelected(tableId: string): void {
    const state = ensure(tableId)
    state.selected.clear()
    state.selectionVersion++
  }

  /**
   * Returns current sort state for a table.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   *
   * Returns:
   * - SortState | null.
   */
  function getSort(tableId: string): SortState | null {
    return ensure(tableId).sort
  }

  /**
   * Toggles sort direction if the same field is clicked, or sets desc for a new field.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   * - field: string - column field name to sort by.
   *
   * Returns:
   * - SortState.
   */
  function toggleSort(tableId: string, field: string): SortState {
    const state = ensure(tableId)

    if (state.sort?.field === field) {
      state.sort = {
        field: field,
        direction: state.sort.direction === "desc" ? "asc" : "desc"
      }
    } else {
      state.sort = {
        field: field,
        direction: "desc"
      }
    }

    return state.sort
  }

  /**
   * Returns current page number for a table.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   *
   * Returns:
   * - number.
   */
  function getPage(tableId: string): number {
    return ensure(tableId).page
  }

  /**
   * Sets current page number for a table.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   * - page: number - page number to set.
   *
   * Returns:
   * - void.
   */
  function setPage(tableId: string, page: number): void {
    ensure(tableId).page = page
  }

  /**
   * Returns current search query for a table.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   *
   * Returns:
   * - string.
   */
  function getSearch(tableId: string): string {
    return ensure(tableId).search
  }

  /**
   * Sets search query for a table.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   * - search: string - search query to set.
   *
   * Returns:
   * - void.
   */
  function setSearch(tableId: string, search: string): void {
    ensure(tableId).search = search
  }

  /**
   * Removes all state for a table.
   *
   * Parameters:
   * - tableId: string - unique identifier of the table.
   *
   * Returns:
   * - void.
   */
  function clear(tableId: string): void {
    tables.value.delete(tableId)
  }

  return {
    tables,
    getSelected,
    getSelectionVersion,
    isSelected,
    isAllSelected,
    toggleItemSelection,
    toggleAllSelection,
    clearSelected,
    getSort,
    toggleSort,
    getPage,
    setPage,
    getSearch,
    setSearch,
    clear
  }
})