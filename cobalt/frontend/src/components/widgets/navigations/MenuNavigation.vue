<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <nav class="menu" :class="{ open }">
    <ul class="header">
      <li class="image">
        <div class="icon">
          <img :src="logoIcon" alt="Logo"/>
        </div>
      </li>
      <li class="text">
        <h2>Cobalt</h2>
        <p>created by Artorias</p>
      </li>
    </ul>
    <div class="group general-menu">
      <h3>{{ $t('nav.menu.general') }}</h3>
      <ul class="items">
        <template v-for="button in generalButtons" :key="button.text">
          <li class="item" v-if="button.isVisible">
            <GhostButton
              :type="button.type"
              :icon="button.icon"
              :text="button.text"
              :base-color="button.baseColor"
              :hover-color="button.hoverColor"
              :to="button.url"
              :name="button.name"
              @click="emit('close')"
            />
          </li>
        </template>
      </ul>
    </div>
    <div class="group banners">
      <SourcesBanner/>
      <SupportBanner/>
    </div>
    <div class="group other-menu">
      <h3>{{ $t('nav.menu.other') }}</h3>
      <ul class="items">
        <li class="item" v-for="button in otherButtons" :key="button.text">
          <GhostButton
            :type="button.type"
            :icon="button.icon"
            :text="button.text"
            :base-color="button.baseColor"
            :hover-color="button.hoverColor"
            :href="button.external ? button.url : undefined"
            :target="button.external ? '_blank' : undefined"
            :name="button.name"
            @click="button.action"
          />
        </li>
      </ul>
    </div>
  </nav>
  <div v-if="open" class="overlay" @click="emit('close')"/>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { computed, inject } from "vue"
import { useRouter } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"

import { useUserStore } from "@/stores"
import { HTTP_AUTH_API_SERVICE_KEY, WS_CLIENT_KEY } from "@/utils"
import { type MenuButton, PermissionEnum, RouteEnum } from "@/types"

import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import SourcesBanner from "@/components/widgets/banners/SourcesBanner.vue"
import SupportBanner from "@/components/widgets/banners/SupportBanner.vue"
import logoIcon from "@/assets/images/svg/logo.svg"
import dashboardIcon from "@/assets/images/svg/dashboard.svg?raw"
import serversIcon from "@/assets/images/svg/servers.svg?raw"
import usersIcon from "@/assets/images/svg/users.svg?raw"
import rolesIcon from "@/assets/images/svg/roles.svg?raw"
import settingsIcon from "@/assets/images/svg/settings.svg?raw"
import helpIcon from "@/assets/images/svg/help.svg?raw"
import logoutIcon from "@/assets/images/svg/logout.svg?raw"

defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  (e: "close"): void
}>()

const httpAuthApiService = inject(HTTP_AUTH_API_SERVICE_KEY)!
const wsClient = inject(WS_CLIENT_KEY)!
const userStore = useUserStore()
const { notify } = useNotification()
const { t } = useI18n()
const router = useRouter()

const generalButtons = computed((): Array<MenuButton> => [
  {
    type: "router-link",
    text: t("nav.menu.dashboard"),
    url: '/',
    icon: dashboardIcon,
    baseColor: "gray",
    hoverColor: "blue",
    name: "dashboard",
    isVisible: hasDashboardViewAccess.value
  },
  {
    type: "router-link",
    text: t("nav.menu.servers"),
    url: "/servers",
    icon: serversIcon,
    baseColor: "gray",
    hoverColor: "blue",
    name: "servers",
    isVisible: hasServersViewAccess.value
  },
  {
    type: "router-link",
    text: t("nav.menu.users"),
    url: "/users",
    icon: usersIcon,
    baseColor: "gray",
    hoverColor: "blue",
    name: "users",
    isVisible: hasUsersViewAccess.value
  },
  {
    type: "router-link",
    text: t("nav.menu.roles"),
    url: "/roles",
    icon: rolesIcon,
    baseColor: "gray",
    hoverColor: "blue",
    name: "roles",
    isVisible: hasRolesViewAccess.value
  },
  {
    type: "router-link",
    text: t("nav.menu.settings"),
    url: "/settings",
    icon: settingsIcon,
    baseColor: "gray",
    hoverColor: "blue",
    name: "settings",
    isVisible: userStore.user !== null
  }
])

const otherButtons = computed((): Array<MenuButton> => [
  {
    type: "a",
    text: t("nav.menu.help"),
    url: "https://github.com/artorias-developer/cobalt/discussions/categories/help",
    icon: helpIcon,
    baseColor: "gray",
    hoverColor: "blue",
    external: true,
    name: "help"
  },
  {
    type: "button",
    text: t("nav.menu.logout.label"),
    icon: logoutIcon,
    baseColor: "gray",
    hoverColor: "red",
    name: "logout",
    action: handleLogout
  }
])

/**
 * Handles the user logout action.
 * Calls the auth API to invalidate the session and redirects to the login page.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleLogout(): Promise<void> {
  try {
    await httpAuthApiService.logout()
    userStore.clearUser()
    wsClient.disconnect()

    await router.push({
      name: RouteEnum.LOGIN
    })
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("nav.menu.logout.error")
    })
  }
}

/**
 * Checks whether the current user has access to view dashboard.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasDashboardViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.DASHBOARD_VIEW)
)

/**
 * Checks whether the current user has access to view servers.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServersViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.SERVERS_VIEW)
)

/**
 * Checks whether the current user has access to view users.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasUsersViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.USERS_VIEW)
)

/**
 * Checks whether the current user has access to view roles.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasRolesViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.ROLES_VIEW)
)
</script>

<style scoped lang="scss">
.menu {
  width: 100%;
  height: 100%;
  max-width: 276px;
  display: flex;
  flex-direction: column;
  gap: $space-xl;
  padding: $space-xl;
  border-right: 1px solid var(--color-border-alt);
  overflow-y: auto;
  overscroll-behavior: none;
  @include scrollbar-hidden();
  box-sizing: border-box;

  .header {
    height: 60px;
    display: flex;
    align-items: center;
    gap: $space-md;
    padding: 0 $space-md;

    .image {
      .icon {
        width: 30px;
        height: 30px;

        img {
          width: 100%;
          height: 100%;
        }
      }
    }

    .text {
      display: flex;
      flex-direction: column;
      gap: $space-sm;

      h2 {
        font-size: $font-xxl;
        font-weight: 700;
        color: var(--color-title);
        line-height: 1;
      }

      p {
        font-size: $font-sm;
        font-weight: 600;
        color: var(--color-description);
        line-height: 1;
        text-wrap: nowrap;
      }
    }
  }

  .group {
    h3 {
      font-size: $font-xs;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--color-description);
      padding-left: $space-md;
      margin-bottom: $space-md;
    }

    .items {
      display: flex;
      flex-direction: column;
      gap: $space-md;

      .item {
        .button {
          width: 100%;
        }
      }
    }

    &.banners {
      display: flex;
      flex-direction: column;
      gap: $space-md;
    }

    &.other-menu {
      margin-top: auto;
    }
  }
}

.overlay {
  display: none;
}

@media (max-width: 1024px) {
  .menu {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    height: 100dvh;
    z-index: 100;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    background-color: var(--color-background);

    &.open {
      transform: translateX(0);
    }
  }

  .overlay {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 99;
    background-color: rgba(0, 0, 0, 0.5);
  }
}

@media (max-width: 768px) {
  .menu {
    gap: $space-lg;
    padding: $space-lg;
  }
}
</style>