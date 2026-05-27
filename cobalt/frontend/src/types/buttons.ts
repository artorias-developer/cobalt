/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { Color } from "@/types"

export type ButtonType = "router-link" | "a" | "button"
export type ButtonTarget = "_blank" | "_self" | "_parent" | "_top"
export type ButtonAlign = "start" | "center"

export type WalletNetwork = {
  name: string
  address: string
  icon?: string
}

export type WalletButton = {
  name: string
  icon: string
  networks: Array<WalletNetwork>
  baseColor: Color
  hoverColor: Color
}

export type MenuButton = {
  type: ButtonType
  name: string
  icon: string
  baseColor: Color
  hoverColor: Color
  isVisible?: boolean
  external?: boolean
  url?: string
  action?: () => void
}

export type ActionsMenuButton = {
  label: string
  icon: string
  danger?: boolean
  action: () => void
}