<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div
    v-if="hasServerViewAccess"
    class="page"
    :class="server?.game.name"
  >
    <div class="heading">
      <div class="info">
        <h1>{{ server?.name || "Unknown" }}</h1>
        <div class="tags">
          <span
            v-for="tag in tags"
            :key="tag.label"
            class="tag"
            :class="tag.class"
          >
            {{ tag.label }}
          </span>
        </div>
      </div>
    </div>
    <component
      v-if="serverComponent"
      :is="serverComponent"
      :server-id="serverId"
    />
  </div>
  <NotFound v-else/>
</template>

<script setup lang="ts">
import { computed, onMounted, inject } from "vue"
import { useRoute } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"
import type { Component } from "vue"

import { useUserStore, useServerStore } from "@/stores"
import { GameModules, HTTP_SERVERS_API_SERVICE_KEY } from "@/utils"
import { PermissionsEnum } from "@/types"
import type { Tag, ServerEntity, ServerStatusEntity } from "@/types"

import NotFound from "@/components/widgets/NotFound.vue"

import DontStarveTogetherServerPage from "@/pages/games/dont-starve-together/ServerPage.vue"
import FactorioServerPage from "@/pages/games/factorio/ServerPage.vue"
import MinecraftServerPage from "@/pages/games/minecraft/ServerPage.vue"
import TerrariaServerPage from "@/pages/games/terraria/ServerPage.vue"
import RimWorldServerPage from "@/pages/games/rim-world/ServerPage.vue"

const gameComponents: Record<string, Component> = {
  dont_starve_together: DontStarveTogetherServerPage,
  factorio: FactorioServerPage,
  minecraft: MinecraftServerPage,
  terraria: TerrariaServerPage,
  rim_world: RimWorldServerPage
}

const httpServersApiService = inject(HTTP_SERVERS_API_SERVICE_KEY)!
const userStore = useUserStore()
const serverStore = useServerStore()
const { notify } = useNotification()
const route = useRoute()

/**
 * Fetches the server data from the API and saves it to the store.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchServer(): Promise<void> {
  try {
    const data = await httpServersApiService.getOne(serverId.value)
    serverStore.setServer(serverId.value, data)
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to fetch server"
    })
  }
}

/**
 * Fetches the server container status from the API and saves it to the store.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchServerStatus(): Promise<void> {
  try {
    const data = await httpServersApiService.status(serverId.value)
    serverStore.setStatus(serverId.value, data)
    serverStore.setHostname(serverId.value, window.location.hostname)
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to fetch server status"
    })
  }
}

/**
 * Returns the server page component based on the game name from the route.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Component | null: Game-specific server page component, or null if not found.
 */
const serverComponent = computed((): Component | null =>
  gameComponents[route.params.game as string] ?? null
)

/**
 * Returns the current server ID based on url.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - number: Current server ID.
 */
const serverId = computed((): number =>
  Number(route.params.server_id)
)

/**
 * Returns the server entity from the store for the current server ID.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - ServerEntity | null.
 */
const server = computed((): ServerEntity | null =>
  serverStore.getServer(serverId.value)
)

/**
 * Returns the status entity from the store for the current server ID.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - ServerStatusEntity | null.
 */
const status = computed((): ServerStatusEntity | null =>
  serverStore.getStatus(serverId.value)
)

/**
 * Returns the list of tags to display in the server info section.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Tag[]: Array of tag objects with label and optional class.
 */
const tags = computed((): Tag[] => {
  const gameName = server.value?.game.name ?? ""
  const loaderName = server.value?.loader.name ?? ""

  return [
    {
      label: status.value?.running ? "Online" : "Offline",
      class: status.value?.running ? "green" : "red"
    },
    {
      label: GameModules[gameName]?.displayName
    },
    {
      label: GameModules[gameName]?.loaders[loaderName]?.displayName
    },
    {
      label: server.value?.version
    }
  ].filter(
    tag => tag.label != undefined
  )
})

/**
 * Checks whether the current user has access to view the server.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServerViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SERVER_VIEW)
)

onMounted(async (): Promise<void> => {
  if (hasServerViewAccess.value) {
    await Promise.all([
      fetchServer(),
      fetchServerStatus()
    ])
  }
})
</script>

<style scoped lang="scss">
.page {
  .heading {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: $space-xl;

    .info {
      display: flex;
      flex-direction: column;
      gap: $space-xl;

      h1 {
        color: $color-title;
        font-size: $font-xxxl;
        font-weight: 700;
      }

      .tags {
        display: flex;
        flex-wrap: wrap;
        gap: $space-md;

        .tag {
          color: $color-text;
          background-color: $color-tag-background;
          font-size: $font-md;
          font-weight: 600;
          padding: $space-sm $space-md;
          border-radius: 50px;

          &.green {
            color: $color-green;
            background-color: $color-green-background;
          }

          &.red {
            color: $color-red;
            background-color: $color-red-background;
          }
        }
      }
    }
  }
}

@media (max-width: 1024px) {
  .page {
    .heading {
      margin-top: $space-xl;
    }
  }
}

@media (max-width: 768px) {
  .page {
    .heading {
      gap: $space-md;

      .info {
        gap: $space-md;

        h1 {
          font-size: $font-xxl;
        }

        .tags {
          .tag {
            font-size: $font-sm;
          }
        }
      }
    }
  }
}
</style>