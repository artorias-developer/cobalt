<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="settings tab">
    <section class="column left">
      <ServerUpgradeBlock
        :server-id="serverId"
      />
    </section>
    <section class="column right">
    </section>
  </div>
</template>

<script setup lang="ts">
import ServerUpgradeBlock from "@/components/widgets/blocks/server/ServerUpgradeBlock.vue"

defineProps<{
  serverId: number
}>()
</script>

<style scoped lang="scss">
.settings {
  height: 100%;
  display: flex;
  gap: $space-xl;

  section {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: $space-xl;
  }
}

@media (max-width: 1280px) {
  .settings {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .settings {
    gap: $space-md;

    section {
      gap: $space-md;
    }
  }
}
</style>