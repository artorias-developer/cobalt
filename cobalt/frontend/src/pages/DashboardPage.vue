<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="page" v-if="hasDashboardViewAccess">
    <section class="metrics">
      <CpuUsageChart
        mode="host"
        :labels-to-show="labelsToShow"
        :max-points="maxPoints"
      />
      <RamUsageChart
        mode="host"
        :labels-to-show="labelsToShow"
        :max-points="maxPoints"
      />
      <DiskUsageChart/>
    </section>
    <section class="console">
      <LogsBlock
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

import CpuUsageChart from "@/components/widgets/charts/CpuUsageChart.vue"
import DiskUsageChart from "@/components/widgets/charts/DiskUsageChart.vue"
import RamUsageChart from "@/components/widgets/charts/RamUsageChart.vue"
import LogsBlock from "@/components/widgets/blocks/LogsBlock.vue"
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