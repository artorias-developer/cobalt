/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { createPinia } from "pinia"
import Notifications from "@kyvg/vue3-notification"
import type { App } from "vue"

import {
  setupI18n,
  setupRouterInstance,
  setupRouterGuard,
  setupThemeWatch,
  setupLanguageWatch,
  setupTimezoneWatch,
  setupRoleUpdateWatch,
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
} from "@/boostrap"
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
} from "@/constants"

/**
 * Sets up all dependency providers for the Vue application.
 * Creates and provides all dependencies to the app instance.
 *
 * Parameters:
 * - app: Vue application instance.
 * - router: Router instance, required by the HTTP client for auth redirects.
 * - t: Translation function, required by the HTTP client for error notifications.
 *
 * Returns:
 * - object: Object containing selected initialized services.
 */
function setupProviders(app: App, router: ReturnType<typeof setupRouterInstance>, t: (key: string) => string) {
  const httpClient = createHttpAxiosClient(router, t)
  const wsClient = createWebSocketClient()

  wsClient.connect(`wss://${window.location.host}/api/v1/ws`)

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

  return { httpUsersApiService, localeHelper, wsClient }
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
  const i18n = setupI18n()
  const router = setupRouterInstance()

  const { httpUsersApiService, localeHelper, wsClient } = setupProviders(app, router, i18n.global.t)
  app.use(createPinia())
  app.use(Notifications)
  app.use(i18n)
  setupRouterGuard(router, httpUsersApiService, i18n)
  app.use(router)
  setupThemeWatch()
  setupLanguageWatch(i18n)
  setupTimezoneWatch(localeHelper)
  setupRoleUpdateWatch(wsClient)
}