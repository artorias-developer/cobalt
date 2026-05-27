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

import PageTabs from "@/components/ui/tabs/PageTabs.vue"
import OverviewTab from "@/components/widgets/server/OverviewTab.vue"
import FilesTab from "@/components/widgets/server/FilesTab.vue"

defineProps<{
  serverId: number
}>()

const activeTab = ref<string | null>(null)

const tabs = [
  {
    label: "Overview",
    value: "overview"
  },
  {
    label: "Files",
    value: "files"
  }
]
</script>

<style lang="scss">
body:has(.page.minecraft) {
  @include background-image(
    $image: "@/assets/images/games/minecraft/background.png"
  );
}
</style>