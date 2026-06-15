/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { watch } from "vue"
import type { App } from "vue"
import { createPinia } from "pinia"
import Notifications from "@kyvg/vue3-notification"
import { useNotification } from "@kyvg/vue3-notification"

import router from "@/router"
import { useUserStore } from "@/stores"

import {
  createHttpAxiosClient,
  createWebSocketClient,
  createDocumentHelper,
  createLocaleHelper,
  createHttpAuthApiService,
  createHttpMetricsApiService,
  createHttpLogsApiService,
  createHttpServersApiService,
  createHttpGamesApiService,
  createHttpRolesApiService,
  createHttpUsersApiService,
  createHttpSettingsApiService,
  createHttpFilesApiService,
  createWsLogsApiService,
  createWsMetricsApiService,
  createWsServersApiService
} from "@/factories"
import {
  WS_CLIENT_KEY,
  DOCUMENT_HELPER_KEY,
  LOCALE_HELPER_KEY,
  HTTP_AUTH_API_SERVICE_KEY,
  HTTP_METRICS_API_SERVICE_KEY,
  HTTP_LOGS_API_SERVICE_KEY,
  HTTP_SERVERS_API_SERVICE_KEY,
  HTTP_GAMES_API_SERVICE_KEY,
  HTTP_ROLES_API_SERVICE_KEY,
  HTTP_USERS_API_SERVICE_KEY,
  HTTP_SETTINGS_API_SERVICE_KEY,
  HTTP_FILES_API_SERVICE_KEY,
  WS_METRICS_API_SERVICE_KEY,
  WS_LOGS_API_SERVICE_KEY,
  WS_SERVERS_API_SERVICE_KEY
} from "@/utils"
import { RoutesEnum } from "@/types"

/**
 * Sets up all dependency providers for the Vue application.
 * Creates and provides all dependencies to the app instance.
 *
 * Parameters:
 * - app: Vue application instance.
 *
 * Returns:
 * - object: Object containing selected initialized services.
 */
function setupProviders(app: App) {
  const httpClient = createHttpAxiosClient()
  const wsClient = createWebSocketClient()

  const documentHelper = createDocumentHelper()
  const localeHelper = createLocaleHelper()

  const httpAuthApiService = createHttpAuthApiService(httpClient)
  const httpMetricsApiService = createHttpMetricsApiService(httpClient)
  const httpLogsApiService = createHttpLogsApiService(httpClient)
  const httpServersApiService = createHttpServersApiService(httpClient)
  const httpGamesApiService = createHttpGamesApiService(httpClient)
  const httpRolesApiService = createHttpRolesApiService(httpClient)
  const httpUsersApiService = createHttpUsersApiService(httpClient)
  const httpSettingsApiService = createHttpSettingsApiService(httpClient)
  const httpFilesApiService = createHttpFilesApiService(httpClient)

  const wsLogsApiService = createWsLogsApiService(wsClient)
  const wsMetricsApiService = createWsMetricsApiService(wsClient)
  const wsServersApiService = createWsServersApiService(wsClient)

  app.provide(WS_CLIENT_KEY, wsClient)

  app.provide(DOCUMENT_HELPER_KEY, documentHelper)
  app.provide(LOCALE_HELPER_KEY, localeHelper)

  app.provide(HTTP_AUTH_API_SERVICE_KEY, httpAuthApiService)
  app.provide(HTTP_METRICS_API_SERVICE_KEY, httpMetricsApiService)
  app.provide(HTTP_LOGS_API_SERVICE_KEY, httpLogsApiService)
  app.provide(HTTP_SERVERS_API_SERVICE_KEY, httpServersApiService)
  app.provide(HTTP_GAMES_API_SERVICE_KEY, httpGamesApiService)
  app.provide(HTTP_ROLES_API_SERVICE_KEY, httpRolesApiService)
  app.provide(HTTP_USERS_API_SERVICE_KEY, httpUsersApiService)
  app.provide(HTTP_SETTINGS_API_SERVICE_KEY, httpSettingsApiService)
  app.provide(HTTP_FILES_API_SERVICE_KEY, httpFilesApiService)

  app.provide(WS_METRICS_API_SERVICE_KEY, wsMetricsApiService)
  app.provide(WS_LOGS_API_SERVICE_KEY, wsLogsApiService)
  app.provide(WS_SERVERS_API_SERVICE_KEY, wsServersApiService)

  wsClient.connect(`wss://${window.location.hostname}/api/v1/ws`)

  return { httpUsersApiService, localeHelper }
}

/**
 * Sets up the router navigation guard that fetches the current user
 * before each route and redirects to login if the session is invalid.
 *
 * Parameters:
 * - httpUsersApiService: HTTP Users API service instance.
 *
 * Returns:
 * - void.
 */
function setupRouter(httpUsersApiService: ReturnType<typeof createHttpUsersApiService>): void {
  router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()
    const { notify } = useNotification()

    if (!userStore.user && to.name !== RoutesEnum.LOGIN) {
      try {
        const user = await httpUsersApiService.getMe()
        userStore.setUser(user)
      } catch (error: any) {
        notify({
          type: "error",
          text: error?.response?.data?.message ?? "Failed to get current user"
        })
      }
    }

    next()
  })
}

/**
 * Sets up a watcher that syncs the user's timezone setting
 * with the LocaleHelper whenever it changes.
 *
 * Parameters:
 * - localeHelper: LocaleHelper instance.
 *
 * Returns:
 * - void.
 */
function setupLocaleSync(localeHelper: ReturnType<typeof createLocaleHelper>): void {
  const userStore = useUserStore()

  watch(
    () => userStore.user?.settings?.timezone,
    (timezone) => {
      if (timezone) localeHelper.setTimezone(timezone)
    }
  )
}

/**
 * Bootstraps the Vue application.
 *
 * Parameters:
 * - app: Vue application instance.
 *
 * Returns:
 * - void.
 */
export function bootstrap(app: App): void {
  const { httpUsersApiService, localeHelper } = setupProviders(app)
  app.use(createPinia())
  app.use(Notifications)
  setupRouter(httpUsersApiService)
  app.use(router)
  setupLocaleSync(localeHelper)
}