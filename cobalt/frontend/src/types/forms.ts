/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { PermissionsEnum } from "@/types"

export type FormContext = {
  register: (id: symbol, field: FormField) => void
  unregister: (id: symbol) => void
}

export type FormField = {
  name: string
  getValue: () => any
}

export type RadioOption = {
  value: string | number
  title: string
  description?: string
  icon?: string
}

export type SelectOption = {
  value: string | number
  label: string
  icon?: string
}

export type PermissionOption = {
  value: PermissionsEnum
  label: string
}

export type PermissionGroup = {
  label: string
  permissions: PermissionOption[]
}