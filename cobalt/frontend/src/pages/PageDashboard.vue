<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="page" v-if="hasDashboardViewAccess" data-id="cbc8ade746f56b6a385d97a58f08ccb77ce606e643f">
    <section class="metrics">
      <ChartCpuUsage
        mode="host"
        :labels-to-show="labelsToShow"
        :max-points="maxPoints"
      />
      <ChartRamUsage
        mode="host"
        :labels-to-show="labelsToShow"
        :max-points="maxPoints"
      />
      <ChartDiskUsage/>
    </section>
    <section class="console">
      <BlockLogs
        mode="host"
        :max-logs="maxLogs"
      />
    </section>
  </div>
  <NotFound v-else/>
</template>

<script setup lang="ts">
import { computed } from "vue"

import { useUserStore } from "@/stores"
import { PermissionEnum } from "@/types"

import ChartCpuUsage from "@/components/widgets/charts/ChartCpuUsage.vue"
import ChartDiskUsage from "@/components/widgets/charts/ChartDiskUsage.vue"
import ChartRamUsage from "@/components/widgets/charts/ChartRamUsage.vue"
import BlockLogs from "@/components/widgets/blocks/BlockLogs.vue"
import NotFound from "@/components/widgets/NotFound.vue"

const userStore = useUserStore()

const maxPoints = 300
const maxLogs = 300
const labelsToShow = 4

/**
 * Checks whether the current user has access to view dashboard.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasDashboardViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.DASHBOARD_VIEW)
)
</script>

<style scoped lang="scss">
.page {
  display: flex;
  flex-direction: column;
  height: 100%;

  section {
    display: flex;
    justify-content: space-between;
    gap: $space-xl;

    &.console {
      flex: 1;
      min-height: 0;
    }
  }
}

@media (max-width: 1550px) {
  .page {
    section {
      &.metrics {
        flex-wrap: wrap;

        :deep(.cpu) {
          order: 1;
          width: 100%;
        }

        :deep(.ram) {
          order: 2;
          flex: 1;
        }

        :deep(.disk) {
          order: 3;
          flex: 1;
        }
      }
    }
  }
}

@media (max-width: 1150px) {
  .page {
    section {
      &.metrics {
        :deep(.cpu),
        :deep(.ram),
        :deep(.disk) {
          width: 100%;
          flex: none;
        }
      }
    }
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