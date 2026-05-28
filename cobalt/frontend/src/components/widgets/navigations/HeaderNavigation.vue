<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="header">
    <ul class="logo">
      <li class="image">
        <div class="icon">
          <img :src="logoIcon" alt="Logo"/>
        </div>
      </li>
      <li class="text">
        <h2>Cobalt</h2>
      </li>
    </ul>
    <nav class="breadcrumbs">
      <span class="crumb root">Cobalt</span>
      <span class="separator">/</span>
      <span class="crumb current">{{ currentRoute }}</span>
    </nav>
    <div class="buttons">
      <template v-for="button in buttons" :key="button.text">
        <GhostButton
          type="router-link"
          v-if="button.isVisible"
          :icon="button.icon"
          :base-color="button.baseColor"
          :hover-color="button.hoverColor"
          :filled="true"
          :to="button.url"
          align="center"
        />
      </template>
      <GhostButton
        type="button"
        class="burger"
        :icon="menuIcon"
        base-color="gray"
        hover-color="gray"
        :filled="true"
        align="center"
        @click="emit('toggle-menu')"
      />
    </div>
  </Block>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"

import { useUserStore } from "@/stores"
import { PermissionsEnum } from "@/types"
import type { MenuButton } from "@/types"

import Block from "@/components/ui/Block.vue"
import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import logoIcon from "@/assets/images/svg/logo.svg"
import settingsIcon from "@/assets/images/svg/settings.svg?raw"
import usersIcon from "@/assets/images/svg/users.svg?raw"
import menuIcon from "@/assets/images/svg/menu.svg?raw"

const emit = defineEmits<{
  (e: "toggle-menu"): void
}>()

const userStore = useUserStore()
const route = useRoute()

const buttons = computed((): Array<MenuButton> => [
  {
    type: "router-link",
    text: "Profile",
    url: "/settings?tab=security",
    icon: usersIcon,
    baseColor: "gray",
    hoverColor: "gray",
    isVisible: userStore.user !== null
  },
  {
    type: "router-link",
    text: "Settings",
    url: "/settings?tab=system",
    icon: settingsIcon,
    baseColor: "gray",
    hoverColor: "gray",
    isVisible: hasSettingsSystemAccess.value
  }
])

/**
 * Computes a string representing the current route.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - string: The current route name or the last segment of the path, or "" if unavailable.
 */
const currentRoute = computed((): string => {
  return route.name?.toString() ?? route.path.split("/").filter(Boolean).pop() ?? ""
})

/**
 * Checks whether the current user has access to system settings.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasSettingsSystemAccess = computed((): boolean =>
  userStore.hasAnyPermission([
    PermissionsEnum.SETTINGS_CACHE_CLEAR,
    PermissionsEnum.SETTINGS_CONTAINERS_CLEAR
  ])
)
</script>

<style scoped lang="scss">
.header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: $space-md $space-xl;

  .logo {
    display: none;
  }

  .breadcrumbs {
    display: flex;
    align-items: center;
    gap: 8px;

    .crumb {
      font-size: $font-sm;
      font-weight: 600;

      &.root {
        color: $color-text;
      }

      &.current {
        color: $color-title;
      }
    }

    .separator {
      color: $color-text;
      font-size: $font-sm;
    }
  }

  .buttons {
    display: flex;
    gap: $space-md;

    .burger {
      display: none;
    }
  }
}

@media (max-width: 1024px) {
  .header {
    .logo {
      display: flex;
      align-items: center;
      gap: $space-md;

      .image {
        .icon {
          width: 26px;
          height: 26px;

          img {
            width: 100%;
            height: 100%;
          }
        }
      }

      .text {
        h2 {
          font-size: $font-lg;
          font-weight: 700;
          color: $color-title;
          line-height: 1;
        }
      }
    }

    .breadcrumbs {
      display: none;
    }

    .buttons {
      .burger {
        display: flex;
      }

      :deep(.button:not(.burger)) {
        display: none;
      }
    }
  }
}

@media (max-width: 768px) {
  .header {
    padding: $space-md $space-lg;
  }
}
</style>