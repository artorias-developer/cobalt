<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="files tab">
    <section class="explorer">
      <FilesBlock
        :key="server?.id ?? 'none'"
        :mode="server?.id ? 'server' : 'empty'"
        :server-id="server?.id"
      />
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"

import { useServerStore } from "@/stores"

import FilesBlock from "@/components/widgets/blocks/FilesBlock.vue"

const props = defineProps<{
  serverId: number
}>()

const serverStore = useServerStore()

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
</script>

<style scoped lang="scss">
.files {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: $space-xl;

  section {
    display: flex;
    flex-direction: column;
    gap: $space-xl;

    &.explorer {
      width: 100%;
      flex: 1;
      min-height: 0;

      :deep(.files) {
        flex: 1;

        .wrapper {
          flex: 1;
          min-height: 0;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .files {
    gap: $space-md;

    section {
      gap: $space-md;
    }
  }
}
</style>