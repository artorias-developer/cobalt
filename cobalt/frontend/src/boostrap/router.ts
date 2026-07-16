/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { createRouter, createWebHistory } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"

import { useUserStore } from "@/stores"
import { RouteEnum } from "@/types"

import LoginPage from "@/pages/LoginPage.vue"
import DashboardPage from "@/pages/DashboardPage.vue"
import ServersPage from "@/pages/ServersPage.vue"
import ServerPage from "@/pages/ServerPage.vue"
import UsersPage from "@/pages/UsersPage.vue"
import RolesPage from "@/pages/RolesPage.vue"
import SettingsPage from "@/pages/SettingsPage.vue"
import NotFoundPage from "@/pages/NotFoundPage.vue"

import type { createHttpUsersApiService } from "@/boostrap/factories"
import type { setupI18n } from "@/boostrap"

/**
 * Defines the application's route table, mapping URL paths
 * to their corresponding page components.
 */
const routes = [
  {
    path: "/login",
    name: RouteEnum.LOGIN,
    component: LoginPage
  },
  {
    path: "/",
    name: RouteEnum.DASHBOARD,
    component: DashboardPage
  },
  {
    path: "/servers",
    name: RouteEnum.SERVERS,
    component: ServersPage
  },
  {
    path: "/servers/:game/:server_id",
    name: RouteEnum.SERVER,
    component: ServerPage
  },
  {
    path: "/users",
    name: RouteEnum.USERS,
    component: UsersPage
  },
  {
    path: "/roles",
    name: RouteEnum.ROLES,
    component: RolesPage
  },
  {
    path: "/settings",
    name: RouteEnum.SETTINGS,
    component: SettingsPage
  },
  {
    path: "/:pathMatch(.*)*",
    name: RouteEnum.NOT_FOUND,
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
export function setupRouterInstance() {
  return createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
  })
}

/**
 * Sets up the router navigation guard that fetches the current user
 * before each route and redirects to login if the session is invalid.
 *
 * Parameters:
 * - router: Router instance to attach the guard to.
 * - httpUsersApiService: HTTP Users API service instance.
 * - i18n: The vue-i18n instance, used for error message translation.
 *
 * Returns:
 * - void.
 */
export function setupRouterGuard(
  router: ReturnType<typeof setupRouterInstance>,
  httpUsersApiService: ReturnType<typeof createHttpUsersApiService>,
  i18n: ReturnType<typeof setupI18n>
): void {
  router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()
    const { notify } = useNotification()

    if (!userStore.user && to.name !== RouteEnum.LOGIN) {
      try {
        const user = await httpUsersApiService.getMe()
        userStore.setUser(user)
      } catch (error: any) {
        notify({
          type: "error",
          text: error?.response?.data?.message ?? i18n.global.t("auth.user.fetch.error")
        })
      }
    }

    next()
  })
}