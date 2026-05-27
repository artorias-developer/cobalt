/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { createRouter, createWebHistory } from "vue-router"

import { RoutesEnum } from "@/types"

import LoginPage from "@/pages/LoginPage.vue"
import DashboardPage from "@/pages/DashboardPage.vue"
import ServersPage from "@/pages/ServersPage.vue"
import ServerPage from "@/pages/ServerPage.vue"
import UsersPage from "@/pages/UsersPage.vue"
import RolesPage from "@/pages/RolesPage.vue"
import SettingsPage from "@/pages/SettingsPage.vue"
import NotFoundPage from "@/pages/NotFoundPage.vue"

const routes = [
  {
    path: "/login",
    name: RoutesEnum.LOGIN,
    component: LoginPage
  },
  {
    path: '/',
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

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
