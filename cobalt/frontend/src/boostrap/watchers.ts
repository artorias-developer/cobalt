/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { watch } from "vue"
import type { Composer } from "vue-i18n"

import { useUserStore } from "@/stores"
import { CookieEnum, LanguageEnum, RoleEventEnum } from "@/types"
import type { RoleEntity, WsMessageEntity } from "@/types"

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
      const cookieMatch = document.cookie.match(
        new RegExp(`(?:^|; )${CookieEnum.LANGUAGE_KEY}=([^;]*)`)
      )
      const resolvedLanguage = language ?? (cookieMatch?.[1] ? decodeURIComponent(cookieMatch[1]) : undefined)

      if (resolvedLanguage) {
        (i18n.global as unknown as Composer).locale.value = resolvedLanguage as LanguageEnum
      }
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
 * The backend sends them only to connections of affected users,
 * so the received role is applied to the store as is.
 *
 * Parameters:
 * - wsClient: WebSocket client instance.
 *
 * Returns:
 * - void.
 */
export function setupRoleUpdateWatch(wsClient: ReturnType<typeof createWebSocketClient>): void {
  const userStore = useUserStore()

  const onRoleUpdate = (event: WsMessageEntity<RoleEntity>) => userStore.setUserRole(event.data)

  wsClient.listen(RoleEventEnum.ROLE_UPDATE, onRoleUpdate)
  wsClient.listen(RoleEventEnum.USER_ROLE_UPDATE, onRoleUpdate)
}