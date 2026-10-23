/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { Color } from "@/types"

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

type MenuButtonBase = {
  text?: string
  icon: string
  baseColor: Color
  hoverColor: Color
  name?: string
  isVisible?: boolean
}

export type RouteMenuButton = MenuButtonBase & {
  type: "router-link"
  url: string
}

export type LinkMenuButton = MenuButtonBase & {
  type: "a"
  url: string
  external?: boolean
}

export type ActionMenuButton = MenuButtonBase & {
  type: "button"
  action: () => void
}

export type MenuButton = RouteMenuButton | LinkMenuButton | ActionMenuButton

export type ActionsMenuButton = {
  label: string
  icon: string
  name?: string
  danger?: boolean
  action: () => void
}