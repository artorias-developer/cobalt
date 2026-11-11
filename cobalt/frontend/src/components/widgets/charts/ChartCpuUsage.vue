<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="cpu" padded gapped>
    <Header
      :icon="icon"
      :icon-color="iconColor"
      :title="title ?? $t('metrics.cpu.title')"
      :description="description ?? $t('metrics.cpu.description')"
      :size="size"
      :icon-filled="filled"
    />
    <Message
      v-if="mode !== 'empty' && !hasCpuViewAccess"
      :icon="padlockIcon"
      :text="$t('common.accessDenied')"
    />
    <Message
      v-else-if="mode === 'empty'"
      :icon="listIcon"
      :text="$t('common.noData')"
    />
    <ChartLine
      v-else
      ref="chartRef"
      :color="color"
      :labels-to-show="labelsToShow"
      :max-points="maxPoints"
    />
  </Block>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { ref, computed, watch, onMounted, onUnmounted, inject } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { useUserStore } from "@/stores"
import { LOCALE_HELPER_KEY, WS_METRICS_API_SERVICE_KEY, HTTP_METRICS_API_SERVICE_KEY } from "@/constants"
import { PermissionEnum } from "@/types"
import type {
  UniversalBlockMode,
  Color,
  BlockHeaderSize,
  MetricEntity,
  WsMessageEntity,
  WsServerMessageEntity
} from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import ChartLine from "@/components/ui/charts/ChartLine.vue"
import Message from "@/components/ui/Message.vue"

import cpuIcon from "@/assets/images/svg/cpu.svg?raw"
import padlockIcon from "@/assets/images/svg/padlock.svg?raw"
import listIcon from "@/assets/images/svg/clipboard-blank.svg?raw"

const props = withDefaults(defineProps<{
  mode: UniversalBlockMode
  serverId?: number
  color?: Color
  icon?: string
  iconColor?: Color
  title?: string
  description?: string
  size?: BlockHeaderSize
  filled?: boolean
  labelsToShow: number
  maxPoints: number
}>(), {
  serverId: undefined,
  color: "blue",
  icon: cpuIcon,
  iconColor: "blue",
  size: "large",
  filled: true
})

const localeHelper = inject(LOCALE_HELPER_KEY)!
const wsMetricsApiService = inject(WS_METRICS_API_SERVICE_KEY)!
const httpMetricsApiService = inject(HTTP_METRICS_API_SERVICE_KEY)!
const userStore = useUserStore()
const { notify } = useNotification()
const { t } = useI18n()

const chartRef = ref<InstanceType<typeof ChartLine> | null>(null)

/**
 * Fetches initial CPU metrics from the API and initializes the chart.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchInitialData(): Promise<void> {
  try {
    await chartRef.value?.initChart([])
    chartRef.value?.showLoading()

    const data = props.mode === "server"
      ? await httpMetricsApiService.getServerAllCpu(props.serverId!)
      : await httpMetricsApiService.getHostAllCpu()

    const cpuData = data.map((item) => ({
      date: localeHelper.formatTime(item.date),
      value: item.value
    }))

    chartRef.value?.setData(cpuData)
    chartRef.value?.hideLoading()
  } catch (error: any) {
    chartRef.value?.hideLoading()
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("metrics.cpu.fetch.error")
    })
  }
}

/**
 * Handles real-time CPU metric updates received from WebSocket.
 *
 * Parameters:
 * - metric: Metric object containing CPU data and optional server_id.
 *
 * Returns:
 * - void.
 */
function handleMetricUpdate(metric: WsMessageEntity<MetricEntity> | WsServerMessageEntity<MetricEntity>): void {
  if (props.mode === "server" && "server_id" in metric && metric.server_id !== props.serverId) return

  const formattedDate = localeHelper.formatTime(metric.data.date)
  chartRef.value?.addPoint(formattedDate, metric.data.value)
}

/**
 * Checks whether the current user has access to view CPU metrics.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasCpuViewAccess = computed((): boolean =>
  props.mode === "server"
    ? userStore.hasPermission(PermissionEnum.SERVER_CPU_VIEW)
    : userStore.hasPermission(PermissionEnum.DASHBOARD_CPU_VIEW)
)

let isSubscribed = false

/**
 * Loads initial CPU data and subscribes to live updates.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function show(): void {
  if (isSubscribed) return
  isSubscribed = true

  fetchInitialData()

  if (props.mode === "server") {
    wsMetricsApiService.subscribeServerCpu(props.serverId!, handleMetricUpdate)
  } else {
    wsMetricsApiService.subscribeHostCpu(handleMetricUpdate)
  }
}

/**
 * Unsubscribes from live CPU updates.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function hide(): void {
  if (!isSubscribed) return
  isSubscribed = false

  if (props.mode === "server") {
    wsMetricsApiService.unsubscribeServerCpu(props.serverId!, handleMetricUpdate)
  } else {
    wsMetricsApiService.unsubscribeHostCpu(handleMetricUpdate)
  }
}

/**
 * Checks whether the chart should load data and receive live updates.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the chart is active and the user has access, `false` otherwise.
 */
const canView = computed((): boolean =>
  props.mode !== "empty" && hasCpuViewAccess.value
)

watch(
  canView,
  (value) => value ? show() : hide(),
  { flush: "post" }
)

onMounted(() => {
  if (canView.value) show()
})

onUnmounted(hide)
</script>

<style scoped lang="scss">
.cpu {
  height: 100%;
  min-height: 220px;
  max-height: 360px;

  .chart,
  .message {
    height: 100%;
  }

  .message {
    justify-content: center;
  }
}
</style>