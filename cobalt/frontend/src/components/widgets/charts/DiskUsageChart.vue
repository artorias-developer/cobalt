<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="disk" padded gapped>
    <div class="heading">
      <Header
        :icon="icon"
        :icon-color="iconColor"
        :title="title"
        :description="description"
        :size="size"
        :icon-filled="filled"
      />
      <div class="buttons" v-if="hasViewAccess">
        <GhostButton
          type="button"
          :icon="reloadIcon"
          base-color="gray"
          hover-color="gray"
          :filled="true"
          align="center"
          :disabled="isRefreshing"
          name="reload"
          @click="refreshDiskMetrics"
        />
      </div>
    </div>
    <Message
      v-if="!hasViewAccess"
      :icon="padlockIcon"
      text="Access denied"
    />
    <div v-else class="content">
      <div class="total">
        <div class="circle" :class="color">
          <p>{{ percentage }}%</p>
          <span>used</span>
        </div>
        <div class="details">
          <div class="used">
            <p>{{ usedGB }} GB</p>
            <span>used</span>
          </div>
          <div class="free">
            <p>{{ freeGB }} GB free out of {{ totalGB }} GB</p>
          </div>
        </div>
      </div>
      <div class="groups">
        <div class="group-item">
          <div class="dot" :class="color"></div>
          <span class="label">Last check</span>
          <span class="separator">·</span>
          <span class="size">{{ lastCheck }}</span>
        </div>
        <div class="group-item">
          <div class="dot" :class="color"></div>
          <span class="label">Next check</span>
          <span class="separator">·</span>
          <span class="size">{{ nextCheck }}</span>
        </div>
      </div>
    </div>
  </Block>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, inject } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { LOCALE_HELPER_KEY, HTTP_METRICS_API_SERVICE_KEY } from "@/utils"
import { useUserStore } from "@/stores"
import { PermissionsEnum } from "@/types"
import type { Color, BlockHeaderSize } from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import Message from "@/components/ui/Message.vue"
import diskIcon from "@/assets/images/svg/disk.svg?raw"
import reloadIcon from "@/assets/images/svg/reload.svg?raw"
import padlockIcon from "@/assets/images/svg/padlock.svg?raw"

withDefaults(defineProps<{
  color?: Color
  icon?: string
  iconColor?: Color
  title?: string
  description?: string
  size?: BlockHeaderSize
  filled?: boolean
}>(), {
  color: "yellow",
  icon: diskIcon,
  iconColor: "yellow",
  title: "Disk",
  description: "Space usage",
  size: "large",
  filled: true
})

const localeHelper = inject(LOCALE_HELPER_KEY)!
const httpMetricsApiService = inject(HTTP_METRICS_API_SERVICE_KEY)!
const userStore = useUserStore()
const { notify } = useNotification()

const free = ref<number>(0)
const total = ref<number>(0)
const lastCheck = ref<string>("00:00")
const nextCheck = ref<string>("00:00")
const isRefreshing = ref<boolean>(false)

/**
 * Converts bytes to gigabytes.
 *
 * Parameters:
 * - bytes: Number of bytes.
 *
 * Returns:
 * - number: Value in gigabytes rounded to 2 decimal places.
 */
function bytesToGB(bytes: number): number {
  return Math.round((bytes / 1024 / 1024 / 1024) * 100) / 100
}

/**
 * Fetches disk metrics from the API.
 *
 * Parameters:
 * - forceFresh: If true, bypasses cache and fetches fresh data.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchDiskMetrics(forceFresh: boolean = false): Promise<void> {
  try {
    const data = await httpMetricsApiService.getHostDisk(forceFresh)

    free.value = data.free
    total.value = data.total
    lastCheck.value = localeHelper.formatTime(data.last_check)
    nextCheck.value = localeHelper.formatTime(data.next_check)
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to fetch disk metrics"
    })
  }
}

/**
 * Refreshes disk metrics by fetching fresh data from the API.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function refreshDiskMetrics(): Promise<void> {
  isRefreshing.value = true

  try {
    await fetchDiskMetrics(true)

    notify({
      type: "success",
      text: "Disk metrics refreshed successfully"
    })
  } finally {
    isRefreshing.value = false
  }
}

/**
 * Computes the percentage of used storage space.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - number: The percentage of used space rounded to the nearest integer, or 0 if total is 0.
 */
const percentage = computed((): number => {
  if (total.value === 0) return 0
  return Math.round(((total.value - free.value) / total.value) * 100)
})

/**
 * Returns free storage space converted to gigabytes.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - number: Free space in GB.
 */
const freeGB = computed((): number =>
  bytesToGB(free.value)
)

/**
 * Returns total storage space converted to gigabytes.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - number: Total space in GB.
 */
const totalGB = computed((): number =>
  bytesToGB(total.value)
)

/**
 * Returns used storage space converted to gigabytes.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - number: Used space in GB, calculated as total minus free.
 */
const usedGB = computed((): number =>
  bytesToGB(total.value - free.value)
)

/**
 * Checks whether the current user has access to the disk metrics.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.DASHBOARD_DISK_VIEW)
)

onMounted(() => {
  if (hasViewAccess.value) {
    fetchDiskMetrics()
  }
})
</script>

<style scoped lang="scss">
.disk {
  min-height: min-content;

  .heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: $space-xl;
  }

  .content {
    display: flex;
    flex-direction: column;
    gap: $space-xl;

    .total {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: $space-xl;

      .circle {
        width: 125px;
        height: 125px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: $space-sm;
        border: 8px solid;
        border-radius: 100%;
        box-sizing: border-box;

        &.gray {
          border-color: $color-gray;
        }

        &.red {
          border-color: $color-red;
        }

        &.blue {
          border-color: $color-blue;
        }

        &.green {
          border-color: $color-green;
        }

        &.yellow {
          border-color: $color-yellow;
        }

        p, span {
          line-height: 1;
        }

        p {
          font-size: $font-xxl;
          color: $color-title;
          font-weight: 700;
        }

        span {
          font-size: $font-md;
          color: $color-text;
          font-weight: 600;
        }
      }

      .details {
        display: flex;
        flex-direction: column;
        gap: $space-md;
        text-wrap: nowrap;

        .used {
          display: flex;
          align-items: end;
          gap: $space-sm;

          p {
            font-size: $font-xxl;
            color: $color-title;
            font-weight: 700;
            line-height: 1;
          }

          span {
            font-size: $font-md;
            color: $color-text;
            font-weight: 600;
          }
        }

        .free {
          p {
            font-size: $font-md;
            color: $color-text;
            font-weight: 600;
          }
        }
      }
    }

    .groups {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: $space-xl;

      .group-item {
        display: flex;
        align-items: center;
        gap: $space-md;

        .dot {
          width: 6px;
          height: 6px;
          border-radius: 100%;

          &.gray {
            background-color: $color-gray;
          }

          &.red {
            background-color: $color-red;
          }

          &.blue {
            background-color: $color-blue;
          }

          &.green {
            background-color: $color-green;
          }

          &.yellow {
            background-color: $color-yellow;
          }
        }

        .label {
          font-size: $font-md;
          color: $color-title;
          font-weight: 600;
          white-space: nowrap;
        }

        .separator {
          font-size: $font-md;
          color: $color-text;
          font-weight: 600;
        }

        .size {
          font-size: $font-md;
          color: $color-text;
          font-weight: 600;
        }
      }
    }
  }

  .message {
    height: 161px;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .disk {
    .content {
      gap: $space-lg;

      .total {
        gap: $space-lg;

        .circle {
          p {
            font-size: $font-xl;
          }

          span {
            font-size: $font-sm;
          }
        }

        .details {
          .used {
            p {
              font-size: $font-xl;
            }

            span {
              font-size: $font-sm;
            }
          }

          .free {
            p {
              font-size: $font-sm;
            }
          }
        }
      }

      .groups {
        .group-item {
          .label,
          .size {
            font-size: $font-sm;
          }
        }
      }
    }
  }
}

@media (max-width: 576px) {
  .disk {
    .content {
      .total {
        flex-direction: column;

        .details {
          width: 100%;
          align-items: center;

          .used {
            justify-content: center;
          }
        }
      }

      .groups {
        gap: 10px 20px;
      }
    }
  }
}
</style>