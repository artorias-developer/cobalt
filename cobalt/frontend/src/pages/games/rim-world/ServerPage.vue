<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <PageTabs
    v-model="activeTab"
    :tabs="tabs"
    query-key="page"
  >
    <template #overview>
      <OverviewTab
        :server-id="serverId"
        :logs-regex="logsRegex"
      />
    </template>
    <template #files>
      <FilesTab
        :server-id="serverId"
      />
    </template>
  </PageTabs>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useI18n } from "vue-i18n"

import PageTabs from "@/components/ui/tabs/PageTabs.vue"
import OverviewTab from "@/components/widgets/server/OverviewTab.vue"
import FilesTab from "@/components/widgets/server/FilesTab.vue"

defineProps<{
  serverId: number
}>()

const { t } = useI18n()

const activeTab = ref<string | null>(null)
const logsRegex = /^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})\.\d+Z\s+\[\d{2}:\d{2}:\d{2}\]\s+(?:\[(Warning|Error|Info|Debug|Critical)\]\s+>\s+)?(.*)/s

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
body:has(.page.rim_world) {
  @include background-image(
    $opacity: 0.90,
    $image: "@/assets/images/games/rim-world/background.png"
  );
}
</style>