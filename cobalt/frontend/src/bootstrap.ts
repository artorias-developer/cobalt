/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { watch } from "vue"
import { createRouter, createWebHistory } from "vue-router"
import { createI18n } from "vue-i18n"
import { createPinia } from "pinia"
import Notifications from "@kyvg/vue3-notification"
import { useNotification } from "@kyvg/vue3-notification"
import type { App } from "vue"
import type { Composer } from "vue-i18n"

import { useUserStore } from "@/stores"
import { LanguageEnum, RoutesEnum, RolesEventsEnum } from "@/types"
import type { RoleEntity } from "@/types"

import LoginPage from "@/pages/LoginPage.vue"
import DashboardPage from "@/pages/DashboardPage.vue"
import ServersPage from "@/pages/ServersPage.vue"
import ServerPage from "@/pages/ServerPage.vue"
import UsersPage from "@/pages/UsersPage.vue"
import RolesPage from "@/pages/RolesPage.vue"
import SettingsPage from "@/pages/SettingsPage.vue"
import NotFoundPage from "@/pages/NotFoundPage.vue"

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

import en from "@/locales/en.json"
import uk from "@/locales/uk.json"
import ru from "@/locales/ru.json"

type MessageSchema = typeof en

/**
 * Defines the application's route table, mapping URL paths
 * to their corresponding page components.
 */
const routes = [
  {
    path: "/login",
    name: RoutesEnum.LOGIN,
    component: LoginPage
  },
  {
    path: "/",
    name: RoutesEnum.DASHBOARD,
    component: DashboardPage
  },
  {
    path: "/servers",
    name: RoutesEnum.SERVERS,
    component: ServersPage
  },
  {
    path: "/servers/:game/:server_id",
    name: RoutesEnum.SERVER,
    component: ServerPage
  },
  {
    path: "/users",
    name: RoutesEnum.USERS,
    component: UsersPage
  },
  {
    path: "/roles",
    name: RoutesEnum.ROLES,
    component: RolesPage
  },
  {
    path: "/settings",
    name: RoutesEnum.SETTINGS,
    component: SettingsPage
  },
  {
    path: "/:pathMatch(.*)*",
    name: RoutesEnum.NOT_FOUND,
    component: NotFoundPage
  }
]

/**
 * Creates the Vue Router instance using HTML5 history mode
 * and the application's route table.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Router: Configured router instance ready to be used with app.use().
 */
function setupRouterInstance() {
  return createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
  })
}

/**
 * Sets up all dependency providers for the Vue application.
 * Creates and provides all dependencies to the app instance.
 *
 * Parameters:
 * - app: Vue application instance.
 * - router: Router instance, required by the HTTP client for auth redirects.
 *
 * Returns:
 * - object: Object containing selected initialized services.
 */
function setupProviders(app: App, router: ReturnType<typeof setupRouterInstance>) {
  const httpClient = createHttpAxiosClient(router)
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

  wsClient.connect(`wss://${window.location.host}/api/v1/ws`)

  return { httpUsersApiService, localeHelper, wsClient }
}

/**
 * Creates and configures the vue-i18n instance with support for
 * English and Ukrainian locales, including Ukrainian plural rules.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - I18n: Configured i18n instance ready to be used with app.use().
 */
function setupI18n() {
  return createI18n<[MessageSchema], LanguageEnum>({
    legacy: false,
    locale: LanguageEnum.EN,
    fallbackLocale: LanguageEnum.EN,
    pluralRules: {
      [LanguageEnum.UK]: (n: number): number => {
        if (n === 0) return 0
        if (n % 10 === 1 && n % 100 !== 11) return 1
        if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) return 2
        return 3
      },
      [LanguageEnum.RU]: (n: number): number => {
        if (n === 0) return 0
        if (n % 10 === 1 && n % 100 !== 11) return 1
        if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) return 2
        return 3
      },
    },
    messages: { en, uk, ru },
  })
}

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
function setupThemeWatch(): void {
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
function setupLanguageWatch(i18n: ReturnType<typeof setupI18n>): void {
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
function setupTimezoneWatch(localeHelper: ReturnType<typeof createLocaleHelper>): void {
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
 * Sets up the router navigation guard that fetches the current user
 * before each route and redirects to login if the session is invalid.
 *
 * Parameters:
 * - router: Router instance to attach the guard to.
 * - httpUsersApiService: HTTP Users API service instance.
 *
 * Returns:
 * - void.
 */
function setupRouterGuard(
  router: ReturnType<typeof setupRouterInstance>,
  httpUsersApiService: ReturnType<typeof createHttpUsersApiService>
): void {
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
 * Sets up a WebSocket listener for role update events.
 * When a role update is received, checks if the current user's role
 * matches the updated role and applies the changes to the store.
 *
 * Parameters:
 * - wsClient: WebSocket client instance.
 *
 * Returns:
 * - void.
 */
function setupRoleUpdateListener(wsClient: ReturnType<typeof createWebSocketClient>): void {
  const userStore = useUserStore()

  wsClient.listen(RolesEventsEnum.ROLE_UPDATE, (event: any) => {
    const role: RoleEntity = event.data
    if (userStore.user?.role?.id !== role.id) return
    userStore.setUserRole(role)
  })
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

  const { httpUsersApiService, localeHelper, wsClient } = setupProviders(app, router)
  app.use(createPinia())
  app.use(Notifications)
  app.use(i18n)
  setupRouterGuard(router, httpUsersApiService)
  app.use(router)
  setupThemeWatch()
  setupLanguageWatch(i18n)
  setupTimezoneWatch(localeHelper)
  setupRoleUpdateListener(wsClient)
}