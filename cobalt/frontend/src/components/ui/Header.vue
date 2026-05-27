<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="header">
    <Icon
      :icon="icon"
      :base-color="iconColor"
      :filled="iconFilled"
    />
    <div class="text" :class="size ?? 'large'">
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { BlockHeaderSize, Color } from "@/types"

import Icon from "@/components/ui/Icon.vue"

defineProps<{
  icon: string
  iconColor: Color
  title: string
  description: string
  size?: BlockHeaderSize
  iconFilled?: boolean
}>()
</script>

<style scoped lang="scss">
.header {
  display: flex;
  align-items: center;
  gap: $space-md;

  .text {
    display: flex;
    flex-direction: column;
    gap: $space-sm;

    h3, p {
      line-height: 1;
    }

    h3 {
      font-weight: 700;
      color: $color-title;
    }

    p {
      font-weight: 600;
      color: $color-text;
    }

    &.small {
      h3, p {
        font-size: $font-sm;
      }
    }

    &.large {
      h3 {
        font-size: $font-lg;
      }

      p {
        font-size: $font-md;
      }
    }
  }
}

@media (max-width: 768px) {
  .header {
    .text {
      &.large {
        h3 {
          font-size: $font-md;
        }

        p {
          font-size: $font-sm;
        }
      }
    }
  }
}
</style>