/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { Color, SortDirection } from "@/types"

export type TableIconSize = "small" | "medium"

export type TableColumnLabel = {
  value: string
  highlighted?: boolean
}

export type TableColumnSorting = {
  sortable: boolean
  default?: boolean
  field?: string
}

export type TableColumn =
  | {
    field: string
    type: "text"
    params: {
      label: TableColumnLabel
      sorting?: TableColumnSorting
      action?: (row: Record<string, any>) => void
    }
  }
  | {
    field: string
    type: "tag"
    params: {
      label: TableColumnLabel
      color?: Color
      sorting?: TableColumnSorting
      action?: (row: Record<string, any>) => void
    }
  }
  | {
    field: string
    type: "icon-text"
    params: {
      label: TableColumnLabel
      iconField: string
      iconSize: TableIconSize
      sorting?: TableColumnSorting
      action?: (row: Record<string, any>) => void
    }
  }

export type SortState = {
  field: string
  direction: SortDirection
}

export type TableState = {
  selected: Set<string | number>
  selectionVersion: number
  sort: SortState | null
  page: number
  search: string
}