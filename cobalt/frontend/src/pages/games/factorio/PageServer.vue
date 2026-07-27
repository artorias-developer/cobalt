<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <TabsPage
    v-model="activeTab"
    :tabs="tabs"
    query-key="page"
  >
    <template #overview>
      <ServerTabOverview
        :server-id="serverId"
        :logs-regex="logsRegex"
      />
    </template>
    <template #files>
      <ServerTabFiles
        :server-id="serverId"
      />
    </template>
  </TabsPage>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useI18n } from "vue-i18n"

import TabsPage from "@/components/ui/tabs/TabsPage.vue"
import ServerTabOverview from "@/components/widgets/server/tabs/ServerTabOverview.vue"
import ServerTabFiles from "@/components/widgets/server/tabs/ServerTabFiles.vue"

defineProps<{
  serverId: number
}>()

const { t } = useI18n()

const activeTab = ref<string | null>(null)
const logsRegex = /^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})\.\d+Z\s+(?:\d+\.\d+\s+)?(Info|Warning|Error|Debug|Critical)?\s*(.*)/s

const tabs = [
  {
    label: t("servers.server.tabs.overview"),
    value: "overview"
  },
  {
    label: t("servers.server.tabs.files"),
    value: "files"
  }
]
</script>

<style lang="scss">
body:has(.page.factorio) {
  @include background-image(
    $opacity: 0.90,
    $image: "@/assets/images/games/factorio/background.jpg"
  );
}
</style>