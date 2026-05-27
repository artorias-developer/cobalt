<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="chart" ref="chartRef"/>
</template>

<script setup lang="ts">
import { ref, shallowRef, onUnmounted, inject, nextTick } from "vue"
import { use } from "echarts/core"
import { LineChart } from "echarts/charts"
import { GridComponent, TooltipComponent } from "echarts/components"
import { CanvasRenderer } from "echarts/renderers"
import { init, graphic } from "echarts/core"
import type { ECharts } from "echarts/core"
import type { EChartsOption } from "echarts"

use([LineChart, GridComponent, TooltipComponent, CanvasRenderer])

import { DOCUMENT_HELPER_KEY } from "@/utils"
import type { Color, ChartPoint } from "@/types"

const props = defineProps<{
  color: Color
  labelsToShow: number
  maxPoints: number
}>()

defineExpose({
  initChart,
  setData,
  addPoint,
  showLoading,
  hideLoading
})

const documentHelper = inject(DOCUMENT_HELPER_KEY)!

const chartRef = ref<HTMLDivElement | null>(null)
const chart = shallowRef<ECharts | null>(null)
const gradientCache = new Map<string, graphic.LinearGradient>()

let resizeObserver: ResizeObserver | null = null
let resizeTimeout: number | undefined

/**
 * Creates or retrieves a cached linear gradient for the chart area fill.
 *
 * Parameters:
 * - height: The height of the chart area (used for cache key generation).
 *
 * Returns:
 * - graphic.LinearGradient: A vertical gradient from semi-transparent to more transparent color.
 */
function buildGradient(height: number): graphic.LinearGradient {
  const key = `${props.color}-${height}`
  if (gradientCache.has(key)) return gradientCache.get(key)!

  const hexColor = documentHelper.getRootStyle(`--color-${props.color}`)

  const gradient = new graphic.LinearGradient(0, 0, 0, 1, [
    {offset: 0, color: `${hexColor}40`},
    {offset: 1, color: `${hexColor}15`}
  ])

  gradientCache.set(key, gradient)
  return gradient
}

/**
 * Calculates the interval for displaying axis labels to show a specific number of labels.
 *
 * Parameters:
 * - dataLength: The total number of data points on the axis.
 *
 * Returns:
 * - number: The interval value for ECharts axisLabel configuration (always >= 0).
 */
function calculateInterval(dataLength: number): number {
  if (dataLength <= 1 || props.labelsToShow <= 1) return 0

  const step = (dataLength - 1) / (props.labelsToShow - 1)
  const interval = Math.ceil(step) - 1

  return Math.max(0, interval)
}

/**
 * Pads data array with empty points to reach maxPoints length.
 *
 * Parameters:
 * - data: An array of objects containing date labels and numeric values.
 *
 * Returns:
 * - Array: Padded array with empty data points at the beginning.
 */
function padData(data: Array<ChartPoint>): Array<ChartPoint> {
  const paddingNeeded = props.maxPoints - data.length
  if (paddingNeeded <= 0) return data

  const emptyPoints = Array.from({length: paddingNeeded}, () => ({
    date: "00:00",
    value: 0
  }))

  return [...emptyPoints, ...data]
}

/**
 * Creates a complete ECharts configuration object with all styling and data.
 *
 * Parameters:
 * - data: An array of objects containing date labels and numeric values.
 *
 * Returns:
 * - EChartsOption: A complete chart configuration object.
 */
function createOption(data: Array<ChartPoint>): EChartsOption {
  const mainColor = documentHelper.getRootStyle(`--color-${props.color}`)
  const titleColor = documentHelper.getRootStyle("--color-title")
  const textColor = documentHelper.getRootStyle("--color-text")
  const blockColor = documentHelper.getRootStyle("--color-block-alt")
  const borderColor = documentHelper.getRootStyle("--color-border-alt")

  const paddedData = padData(data)
  const chartHeight = chartRef.value?.clientHeight || 220
  const isMobile = window.innerWidth <= 768

  return {
    animation: false,
    grid: {
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      containLabel: false
    },
    tooltip: {
      trigger: "axis",
      backgroundColor: blockColor,
      borderColor: borderColor,
      borderWidth: 1,
      padding: 10,
      axisPointer: {
        type: "line",
        lineStyle: {
          color: textColor
        }
      },
      textStyle: {
        color: textColor,
        fontFamily: "Montserrat",
        fontSize: 14,
        fontWeight: 600
      },
      formatter: (params: any) => {
        const param = Array.isArray(params) ? params[0] : params
        if (!param?.name) return ""
        return `<div style="color: ${titleColor}; font-size: 14px; font-weight: 600; margin-bottom: 4px;">${param.name}</div>${param.value}%`
      }
    },
    xAxis: {
      type: "category",
      boundaryGap: true,
      data: paddedData.map(d => d.date),
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: textColor,
        fontFamily: "Montserrat",
        fontSize: isMobile ? 14 : 16,
        fontWeight: 600,
        margin: 15,
        align: "center",
        showMinLabel: true,
        showMaxLabel: true,
        alignMinLabel: "left",
        alignMaxLabel: "right",
        interval: calculateInterval(paddedData.length)
      },
      splitLine: {
        show: false
      }
    },
    yAxis: {
      type: "value",
      min: 0,
      max: 100,
      interval: 25,
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: textColor,
        fontFamily: "Montserrat",
        fontSize: isMobile ? 14 : 16,
        fontWeight: 600,
        margin: 45,
        align: "left",
        formatter: (value: number) => {
          if (value === 0 || value === 50 || value === 100) {
            return value.toString()
          }
          return ""
        }
      },
      splitLine: {
        lineStyle: {
          color: borderColor
        }
      }
    },
    series: [
      {
        type: "line",
        smooth: 0.4,
        symbol: "circle",
        symbolSize: 0,
        showSymbol: false,
        lineStyle: {
          width: 2.5,
          color: mainColor
        },
        emphasis: {
          focus: "series",
          itemStyle: {
            color: mainColor,
            borderColor: blockColor,
            borderWidth: 2
          }
        },
        areaStyle: {
          color: buildGradient(chartHeight)
        },
        data: paddedData.map(d => d.value)
      }
    ]
  }
}

/**
 * Initializes the chart with initial data and sets up responsive resizing.
 *
 * Parameters:
 * - data: An array of objects containing date labels and numeric values.
 *
 * Returns:
 * - Promise<void>.
 */
async function initChart(data: Array<ChartPoint>): Promise<void> {
  if (!chartRef.value) return

  if (chart.value) {
    setData(data)
    return
  }

  await nextTick()
  cleanup()

  chart.value = init(chartRef.value)

  resizeObserver = new ResizeObserver(() => {
    chart.value?.resize()
  })

  resizeObserver.observe(chartRef.value)
  chart.value.setOption(createOption(data))
}

/**
 * Updates the chart with new data without reinitializing.
 *
 * Parameters:
 * - data: An array of objects containing date labels and numeric values.
 *
 * Returns:
 * - void.
 */
function setData(data: Array<ChartPoint>): void {
  if (!chart.value) return

  const paddedData = padData(data)

  chart.value.setOption({
    xAxis: {
      data: paddedData.map(d => d.date),
      axisLabel: {
        interval: calculateInterval(paddedData.length)
      }
    },
    series: [{
      data: paddedData.map(d => d.value)
    }]
  })
}

/**
 * Adds a new data point to the chart and removes the oldest point if max limit is reached.
 *
 * Parameters:
 * - label: The x-axis label (typically a formatted time string).
 * - value: The numeric value for the y-axis.
 *
 * Returns:
 * - void.
 */
function addPoint(label: string, value: number): void {
  if (!chart.value) return

  const option = chart.value.getOption()
  const xAxis = Array.isArray(option.xAxis) ? option.xAxis[0] : option.xAxis
  const series = Array.isArray(option.series) ? option.series[0] : option.series

  const labels = (xAxis?.data || []) as string[]
  const values = (series?.data || []) as number[]

  labels.push(label)
  values.push(value)

  if (labels.length > props.maxPoints) {
    labels.shift()
    values.shift()
  }

  chart.value.setOption({
    xAxis: {
      data: labels,
      axisLabel: {
        interval: calculateInterval(labels.length)
      }
    },
    series: [{data: values}]
  })
}

/**
 * Shows loading indicator on the chart.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function showLoading(): void {
  const mainColor = documentHelper.getRootStyle(`--color-${props.color}`)
  const textColor = documentHelper.getRootStyle("--color-text")
  const blockColor = documentHelper.getRootStyle("--color-block")

  chart.value?.showLoading("default", {
    text: "Loading...",
    color: mainColor,
    textColor: textColor,
    maskColor: blockColor,
    showSpinner: true,
    spinnerRadius: 10,
    lineWidth: 3,
    fontSize: 14,
    fontWeight: 600,
    fontFamily: "Montserrat",
    zlevel: 0
  })
}

/**
 * Hides loading indicator on the chart.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function hideLoading(): void {
  chart.value?.hideLoading()
}

/**
 * Cleans up chart resources including timers, observers, and chart instance.
 * Called before reinitialization and on component unmount to prevent memory leaks.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function cleanup(): void {
  if (resizeTimeout) {
    clearTimeout(resizeTimeout)
    resizeTimeout = undefined
  }

  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }

  chart.value?.dispose()
  chart.value = null
}

onUnmounted(() => {
  cleanup()
  gradientCache.clear()
})
</script>

<style scoped lang="scss">
.chart {
  width: 100%;
  height: 100%;
}
</style>