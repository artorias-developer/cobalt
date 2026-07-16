/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { watch } from "vue"
import type { Composer } from "vue-i18n"

import { useUserStore } from "@/stores"
import { LanguageEnum, RolesEventEnum } from "@/types"
import type { RoleEntity } from "@/types"

import type { createWebSocketClient, createLocaleHelper } from "@/boostrap/factories"
import type { setupI18n } from "@/boostrap"

/**
 * Watches for changes in user theme settings and syncs
 * the active theme on the document root element.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
export function setupThemeWatch(): void {
  const userStore = useUserStore()

  watch(
    () => userStore.user?.settings?.theme,
    (theme) => {
      if (theme) document.documentElement.setAttribute("data-theme", theme)
    },
    { immediate: true }
  )
}

/**
 * Watches for changes in user language settings and syncs
 * the active locale on the given i18n instance.
 *
 * Parameters:
 * - i18n: The vue-i18n instance to sync locale on.
 *
 * Returns:
 * - void.
 */
export function setupLanguageWatch(i18n: ReturnType<typeof setupI18n>): void {
  const userStore = useUserStore()

  watch(
    () => userStore.user?.settings?.language,
    (language) => {
      if (language) (i18n.global as unknown as Composer).locale.value = language as LanguageEnum
    },
    { immediate: true }
  )
}

/**
 * Watches for changes in user timezone settings and syncs
 * the active timezone on the given locale helper instance.
 *
 * Parameters:
 * - localeHelper: LocaleHelper instance.
 *
 * Returns:
 * - void.
 */
export function setupTimezoneWatch(localeHelper: ReturnType<typeof createLocaleHelper>): void {
  const userStore = useUserStore()

  watch(
    () => userStore.user?.settings?.timezone,
    (timezone) => {
      if (timezone) localeHelper.setTimezone(timezone)
    },
    { immediate: true }
  )
}

/**
 * Watches for WebSocket role update events.
 * When a role update is received, checks if the current user's role
 * matches the updated role and applies the changes to the store.
 *
 * Parameters:
 * - wsClient: WebSocket client instance.
 *
 * Returns:
 * - void.
 */
export function setupRoleUpdateWatch(wsClient: ReturnType<typeof createWebSocketClient>): void {
  const userStore = useUserStore()

  wsClient.listen(RolesEventEnum.ROLE_UPDATE, (event: any) => {
    const role: RoleEntity = event.data
    if (userStore.user?.role?.id !== role.id) return
    userStore.setUserRole(role)
  })
}