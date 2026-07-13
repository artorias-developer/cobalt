<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block v-if="hasServerUpgradeAccess" class="upgrade" padded gapped>
    <Header
      :icon="updateIcon"
      icon-color="blue"
      :title="$t('servers.server.settings.blocks.upgrade.title')"
      :description="$t('servers.server.settings.blocks.upgrade.description')"
      :icon-filled="true"
    />
    <Message
      v-if="isUpgrading"
      :icon="listIcon"
      :text="$t('servers.server.settings.blocks.upgrade.inProgress')"
    />
    <Message
      v-else-if="gameVersions.length === 0"
      :icon="listIcon"
      :text="$t('servers.server.settings.blocks.upgrade.upToDate')"
    />
    <Form
      v-else
      ref="upgradeForm"
      class="form"
      :on-submit="() => upgradeForm?.validate() && handleUpgrade()"
    >
      <Select
        v-model="selectedVersion"
        :options="gameVersions"
        :validationName="$t('servers.server.settings.blocks.upgrade.version.label')"
        :label="$t('servers.server.settings.blocks.upgrade.version.label')"
        :placeholder="$t('servers.server.settings.blocks.upgrade.version.placeholder')"
        name="new-server-version"
        :required="true"
      />
      <SolidButton
        type="button"
        :text="$t('common.upgrade')"
        color="blue"
        name="server-upgrade"
        @click="handleUpgrade()"
      />
    </Form>
  </Block>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { computed, inject, ref } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { useUserStore, useServerStore } from "@/stores"
import { HTTP_SERVERS_API_SERVICE_KEY } from "@/utils"
import { PermissionEnum, ServerStateEnum } from "@/types"
import type { SelectOption } from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import Select from "@/components/ui/forms/Select.vue"
import Message from "@/components/ui/Message.vue"
import Form from "@/components/ui/forms/Form.vue"
import SolidButton from "@/components/ui/forms/buttons/SolidButton.vue"
import updateIcon from "@/assets/images/svg/download-alt.svg?raw"
import listIcon from "@/assets/images/svg/clipboard-blank.svg?raw"

const props = defineProps<{
  serverId: number
}>()

const httpServersApiService = inject(HTTP_SERVERS_API_SERVICE_KEY)!
const serverStore = useServerStore()
const userStore = useUserStore()
const { notify } = useNotification()
const { t } = useI18n()

const upgradeForm = ref<InstanceType<typeof Form> | null>(null)
const selectedVersion = ref<string>("")

/**
 * Returns the server entity from the store for the given server ID.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - ServerEntity | null.
 */
const server = computed(() =>
  serverStore.getServer(props.serverId)
)

/**
 * Checks whether the server is currently in the upgrading state.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the server is upgrading, `false` otherwise.
 */
const isUpgrading = computed((): boolean =>
  serverStore.getState(props.serverId) === ServerStateEnum.UPGRADING
)

/**
 * Builds the list of selectable upgrade versions from the store.
 * Only versions listed before the current one (newer) are shown.
 * If the loader only exposes a single "Latest" version, it's shown as-is.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - SelectOption[]: Available versions for upgrade.
 */
const gameVersions = computed((): SelectOption[] => {
  const versions = serverStore.getLoaderVersions(props.serverId)

  if (versions.length === 1 && versions[0]?.toLowerCase() === "latest") {
    return versions.map(version => ({ value: version, label: version }))
  }

  const currentIndex = versions.findIndex(version => version === server.value?.version)
  const newerVersions = currentIndex === -1 ? versions : versions.slice(0, currentIndex)

  return newerVersions.map(version => ({ value: version, label: version }))
})

/**
 * Checks whether the current user has access to upgrade the server.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServerUpgradeAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.SERVER_UPDATE)
)

/**
 * Sends the upgrade request for the selected version and refreshes the server entity on success.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleUpgrade(): Promise<void> {
  if (!selectedVersion.value) return

  try {
    await httpServersApiService.upgradeOne(props.serverId, {
      version: selectedVersion.value
    })

    notify({
      type: "success",
      text: t("servers.server.settings.upgrade.success")
    })

    selectedVersion.value = ""
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.settings.upgrade.error")
    })
  }
}
</script>

<style scoped lang="scss">
.upgrade {
  min-height: 200px;

  .message {
    height: 100%;
    justify-content: center;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: $space-xl;
  }
}
</style>