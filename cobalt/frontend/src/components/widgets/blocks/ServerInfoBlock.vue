<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="info" padded gapped>
    <Header
      :icon="listIcon"
      icon-color="blue"
      :title="$t('servers.server.overview.control.title')"
      :description="$t('servers.server.overview.control.description')"
      :icon-filled="true"
    />
    <Message
      v-if="fields.length === 0"
      :icon="listBlankIcon"
      :text="$t('common.noData')"
    />
    <div v-else class="fields">
      <div v-for="field in fields" :key="field.label" class="field">
        <span class="label">{{ field.label }}</span>
        <span
          class="value"
          :class="{ copyable: field.copyable }"
          @click="field.copyable && copyValue(field.value)"
        >
          {{ field.value ?? $t('common.unknown') }}
        </span>
      </div>
    </div>
    <div v-if="hasAnyVisibleButton" class="actions">
      <GhostButton
        v-if="!status?.running && hasServerStartAccess"
        type="button"
        :icon="startIcon"
        :text="$t('servers.server.overview.control.start.label')"
        base-color="green"
        hover-color="green"
        :filled="true"
        align="center"
        :disabled="actionLoading"
        name="server-start"
        @click="handleStart"
      />
      <GhostButton
        v-if="status?.running && hasServerStopAccess"
        type="button"
        :icon="stopIcon"
        :text="$t('servers.server.overview.control.stop.label')"
        base-color="red"
        hover-color="red"
        :filled="true"
        align="center"
        :disabled="actionLoading"
        name="server-stop"
        @click="handleStop"
      />
      <GhostButton
        v-if="hasServerStartAccess"
        type="button"
        :icon="restartIcon"
        :text="$t('servers.server.overview.control.restart.label')"
        base-color="gray"
        hover-color="gray"
        :filled="true"
        align="center"
        :disabled="actionLoading"
        name="server-restart"
        @click="handleRestart"
      />
    </div>
    <slot/>
  </Block>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { computed, ref, inject } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { useUserStore, useServerStore } from "@/stores"
import { HTTP_SERVERS_API_SERVICE_KEY } from "@/utils"
import { PermissionsEnum } from "@/types"
import type { InfoField } from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import Message from "@/components/ui/Message.vue"
import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import listIcon from "@/assets/images/svg/list.svg?raw"
import listBlankIcon from "@/assets/images/svg/clipboard-blank.svg?raw"
import startIcon from "@/assets/images/svg/play.svg?raw"
import stopIcon from "@/assets/images/svg/stop.svg?raw"
import restartIcon from "@/assets/images/svg/restart.svg?raw"

const props = defineProps<{
  serverId: number
}>()

const httpServersApiService = inject(HTTP_SERVERS_API_SERVICE_KEY)!
const serverStore = useServerStore()
const userStore = useUserStore()
const { notify } = useNotification()
const { t } = useI18n()

const actionLoading = ref(false)

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
    const data = await httpServersApiService.status(props.serverId)
    serverStore.setStatus(props.serverId, data)
    serverStore.setHostname(props.serverId, window.location.hostname)
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.overview.control.fetchStatus.error")
    })
  }
}

/**
 * Sends a start request for the current server and refreshes status.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleStart(): Promise<void> {
  actionLoading.value = true

  try {
    await httpServersApiService.start(props.serverId)
    await fetchServerStatus()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.overview.control.start.error")
    })
  } finally {
    actionLoading.value = false
  }
}

/**
 * Sends a stop request for the current server and refreshes status.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleStop(): Promise<void> {
  actionLoading.value = true

  try {
    await httpServersApiService.stop(props.serverId)
    await fetchServerStatus()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.overview.control.stop.error")
    })
  } finally {
    actionLoading.value = false
  }
}

/**
 * Sends a restart request for the current server and refreshes status.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleRestart(): Promise<void> {
  actionLoading.value = true

  try {
    await httpServersApiService.restart(props.serverId)
    await fetchServerStatus()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.overview.control.restart.error")
    })
  } finally {
    actionLoading.value = false
  }
}

/**
 * Copies a value to the clipboard and shows a notification.
 *
 * Parameters:
 * - value: String to copy, or null to do nothing.
 *
 * Returns:
 * - Promise<void>.
 */
async function copyValue(value: string | null): Promise<void> {
  if (!value) return

  try {
    await navigator.clipboard.writeText(value)
    notify({
      type: "success",
      text: t("common.copy.success")
    })
  } catch {
    notify({
      type: "error",
      text: t("common.copyError")
    })
  }
}

/**
 * Returns the list of info fields to display.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - InfoField[]: Array of label/value pairs, empty if no data is available.
 */
const fields = computed((): InfoField[] => {
  if (!hostname.value && status.value?.port == null) return []

  return [
    {
      label: t("servers.server.overview.control.ipAddress"),
      value: status.value ? hostname.value : null,
      copyable: true
    },
    {
      label: t("servers.server.overview.control.port"),
      value: status.value?.port != null ? String(status.value.port) : null,
      copyable: true
    }
  ]
})

/**
 * Checks whether at least one action button should be visible.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if any button (start, stop, or restart) is visible, `false` otherwise.
 */
const hasAnyVisibleButton = computed((): boolean => {
  if (!status?.value?.running && hasServerStartAccess.value) return true
  if (status?.value?.running && hasServerStopAccess.value) return true
  if (hasServerStartAccess.value) return true
  return false
})

/**
 * Returns the status entity from the store for the given server ID.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - ServerStatusEntity | null.
 */
const status = computed(() =>
  serverStore.getStatus(props.serverId)
)

/**
 * Returns the hostname from the store for the given server ID.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - string | null.
 */
const hostname = computed((): string | null =>
  serverStore.getHostname(props.serverId)
)

/**
 * Checks whether the current user has access to start and restart the server.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServerStartAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SERVER_START)
)

/**
 * Checks whether the current user has access to stop the server.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServerStopAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SERVER_STOP)
)
</script>

<style scoped lang="scss">
.info {
  .fields {
    display: flex;
    flex-direction: column;
    gap: $space-xl;

    .field {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .label {
        color: $color-text;
        font-size: $font-md;
        font-weight: 600;
      }

      .value {
        color: $color-title;
        font-size: $font-md;
        font-weight: 600;

        &.copyable {
          cursor: pointer;
        }
      }
    }
  }

  .actions {
    display: flex;
    gap: $space-md;

    :deep(.button) {
      width: 100%;
    }
  }

  .message {
    flex: 1;
    min-height: 50px;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .info {
    .fields {
      gap: $space-lg;

      .field {
        .label,
        .value {
          font-size: $font-sm;
        }
      }
    }
  }
}

@media (max-width: 320px) {
  .info {
    .actions {
      flex-wrap: wrap;
    }
  }
}
</style>