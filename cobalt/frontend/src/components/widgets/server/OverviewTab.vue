<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="overview tab">
    <section class="info">
      <ServerInfoBlock
        :server-id="serverId"
      />
      <CpuUsageChart
        :key="serverId ?? 'none'"
        :mode="serverId ? 'server' : 'empty'"
        :server-id="serverId"
        :labels-to-show="labelsToShow"
        :max-points="maxPoints"
      />
      <RamUsageChart
        :key="serverId ?? 'none'"
        :mode="serverId ? 'server' : 'empty'"
        :server-id="serverId"
        :labels-to-show="labelsToShow"
        :max-points="maxPoints"
      />
    </section>
    <section class="console">
      <LogsBlock
        :key="serverId ?? 'none'"
        :mode="serverId ? 'server' : 'empty'"
        :server-id="serverId"
        :title="$t('servers.server.overview.console.title')"
        :description="$t('servers.server.overview.console.description')"
        :max-logs="maxLogs"
        :logs-regex="logsRegex"
      />
    </section>
  </div>
</template>

<script setup lang="ts">
import RamUsageChart from "@/components/widgets/charts/RamUsageChart.vue"
import CpuUsageChart from "@/components/widgets/charts/CpuUsageChart.vue"
import LogsBlock from "@/components/widgets/blocks/LogsBlock.vue"
import ServerInfoBlock from "@/components/widgets/blocks/ServerInfoBlock.vue"

defineProps<{
  serverId: number
  logsRegex?: RegExp
}>()

const maxPoints = 300
const maxLogs = 300
const labelsToShow = 4
</script>

<style scoped lang="scss">
.overview {
  height: 100%;
  display: flex;
  gap: $space-xl;

  section {
    display: flex;
    flex-direction: column;
    gap: $space-xl;

    &.info {
      width: 100%;
      max-width: 450px;
      min-height: 500px;
      overflow-y: auto;
      overscroll-behavior: none;
      @include scrollbar-hidden();

      :deep(.cpu),
      :deep(.ram) {
        flex: 1;
        min-height: 220px;
      }
    }

    &.console {
      width: 100%;
      flex: 1;
      min-height: 0;

      :deep(.logs) {
        flex: 1;
      }
    }
  }
}

@media (max-width: 1280px) {
  .overview {
    flex-direction: column;

    section {
      &.info {
        max-width: unset;
        overflow-y: unset;

        :deep(.cpu),
        :deep(.ram) {
          flex: none;
        }
      }
    }
  }
}

@media (max-width: 1024px) {
  .overview {
    section {
      &.info {
        min-height: unset;
      }
    }
  }
}

@media (max-width: 768px) {
  .overview {
    gap: $space-md;

    section {
      gap: $space-md;
    }
  }
}
</style>