<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="page" v-if="userStore.user">
    <section class="settings">
      <SettingsBlock/>
    </section>
  </div>
  <NotFound v-else/>
</template>

<script setup lang="ts">
import { useUserStore } from "@/stores"

import SettingsBlock from "@/components/widgets/blocks/SettingsBlock.vue"
import NotFound from "@/components/widgets/NotFound.vue"

const userStore = useUserStore()
</script>

<style scoped lang="scss">
.page {
  section {
    height: 100%;
    display: flex;
    justify-content: space-between;
    gap: $space-xl;
  }
}

@media (max-width: 768px) {
  .page {
    section {
      gap: $space-md;
    }
  }
}
</style>