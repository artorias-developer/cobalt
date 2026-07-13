<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div
    v-if="hasServerViewAccess"
    class="page"
    :class="server?.game.name"
    data-id="813b82c9a543e133113b5ddfe6bfd09037718b49d8"
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
import { useI18n } from "vue-i18n"
import { computed, onMounted, inject, onUnmounted } from "vue"
import { useRoute } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"
import type { Component } from "vue"

import { useUserStore, useServerStore } from "@/stores"
import {
  GameModules,
  HTTP_SERVERS_API_SERVICE_KEY,
  HTTP_GAMES_API_SERVICE_KEY,
  WS_SERVERS_API_SERVICE_KEY
} from "@/utils"
import { PermissionEnum, ServerStateEnum } from "@/types"
import type { Tag, ServerEntity, ServerStatusEntity } from "@/types"

import NotFound from "@/components/widgets/NotFound.vue"

import DontStarveTogetherServerPage from "@/pages/games/dont-starve-together/ServerPage.vue"
import FactorioServerPage from "@/pages/games/factorio/ServerPage.vue"
import MinecraftServerPage from "@/pages/games/minecraft/ServerPage.vue"
import ProjectZomboidServerPage from "@/pages/games/project-zomboid/ServerPage.vue"
import RimWorldServerPage from "@/pages/games/rim-world/ServerPage.vue"
import SevenDaysToDieServerPage from "@/pages/games/seven-days-to-die/ServerPage.vue"
import TerrariaServerPage from "@/pages/games/terraria/ServerPage.vue"

const gameComponents: Record<string, Component> = {
  dont_starve_together: DontStarveTogetherServerPage,
  factorio: FactorioServerPage,
  minecraft: MinecraftServerPage,
  project_zomboid: ProjectZomboidServerPage,
  rim_world: RimWorldServerPage,
  seven_days_to_die: SevenDaysToDieServerPage,
  terraria: TerrariaServerPage
}

const httpGamesApiService = inject(HTTP_GAMES_API_SERVICE_KEY)!
const httpServersApiService = inject(HTTP_SERVERS_API_SERVICE_KEY)!
const wsServersApiService = inject(WS_SERVERS_API_SERVICE_KEY)!
const userStore = useUserStore()
const serverStore = useServerStore()
const { notify } = useNotification()
const { t } = useI18n()
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
      text: error?.response?.data?.message ?? t("servers.server.fetch.error")
    })
  }
}

/**
 * Fetches the server container status and IP.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchServerControls(): Promise<void> {
  try {
    const data = await httpServersApiService.status(serverId.value)
    serverStore.setStatus(serverId.value, data)
    serverStore.setHostname(serverId.value, window.location.hostname)
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.overview.control.fetch.error")
    })
  }
}

/**
 * Fetches the game's loaders and saves the matching loader's versions to the store.
 * Requires the server entity to already be present in the store.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchLoaderVersions(): Promise<void> {
  const currentServer = server.value
  if (!currentServer) return

  try {
    const game = await httpGamesApiService.getOne(currentServer.game.id)
    const loader = game.loaders.find(loader => loader.id === currentServer.loader.id)

    serverStore.setLoaderVersions(serverId.value, loader?.versions ?? [])
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.loader.versions.fetch.error")
    })
  }
}

/**
 * Handles servers state updates received from WebSocket.
 *
 * Parameters:
 * - event: Event with updated server state.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleStateUpdate(event: any): Promise<void> {
  const currentServer = server.value

  if (!currentServer) return
  if (currentServer.id !== event.data.server_id) return

  if (event.data.version !== undefined) {
    serverStore.setVersion(serverId.value, event.data.version)
  }

  if (event.data.running !== undefined) {
    serverStore.setRunning(serverId.value, event.data.running)
  }

  if (event.data.state !== undefined) {
    serverStore.setState(serverId.value, event.data.state)
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

  const statusTag: Tag = server.value?.state === ServerStateEnum.UPGRADING
    ? { label: t("servers.server.status.upgrading"), class: "yellow" }
    : {
      label: status.value?.running ? t("servers.server.status.online") : t("servers.server.status.offline"),
      class: status.value?.running ? "green" : "red"
    }

  return [
    statusTag,
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
  userStore.hasPermission(PermissionEnum.SERVER_VIEW)
)

onMounted(async (): Promise<void> => {
  if (hasServerViewAccess.value) {
    await fetchServer()

    if (server.value?.state === ServerStateEnum.UPGRADE_FAILED) {
      notify({
        type: "error",
        text: t("servers.server.oneTime.upgrade.error")
      })
    }

    await Promise.all([
      fetchServerControls(),
      fetchLoaderVersions()
    ])

    wsServersApiService.subscribeStates(handleStateUpdate)
  }
})

onUnmounted(() => {
  wsServersApiService.unsubscribeStates(handleStateUpdate)
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
        color: var(--color-title);
        font-size: $font-xxxl;
        font-weight: 700;
      }

      .tags {
        display: flex;
        flex-wrap: wrap;
        gap: $space-md;

        .tag {
          color: var(--color-description);
          background-color: var(--color-gray-background);
          font-size: $font-md;
          font-weight: 600;
          padding: $space-sm $space-md;
          border-radius: 50px;

          &.green {
            color: var(--color-green);
            background-color: var(--color-green-background);
          }

          &.yellow {
            color: var(--color-yellow);
            background-color: var(--color-yellow-background);
          }

          &.red {
            color: var(--color-red);
            background-color: var(--color-red-background);
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