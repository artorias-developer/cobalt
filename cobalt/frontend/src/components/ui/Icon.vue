<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div
    class="icon"
    :class="[
      baseColor,
      hoverColor ? `hover-${hoverColor}` : '',
      filled ? 'background' : '',
      isActive ? 'active' : ''
    ]"
    v-html="icon"
  />
</template>

<script setup lang="ts">
import type { Color } from "@/types"

defineProps<{
  icon: string
  baseColor: Color
  hoverColor?: Color
  filled?: boolean
  isActive?: boolean
}>()
</script>

<style scoped lang="scss">
.icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 18px;
  height: 18px;
  transition: color 0.3s ease;

  :deep(svg) {
    width: 18px;
    height: 18px;
  }

  &.background {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    transition: background-color 0.3s ease, color 0.3s ease;
  }

  &.gray {
    color: $color-text;

    &.background {
      background-color: $color-gray-background;
    }
  }

  *:hover > &.hover-gray,
  &.active.hover-gray {
    color: $color-text;

    &.background {
      background-color: $color-gray-background;
    }
  }

  &.red {
    color: $color-red;

    &.background {
      background-color: $color-red-background;
    }
  }

  *:hover > &.hover-red,
  &.active.hover-red {
    color: $color-red;

    &.background {
      background-color: $color-red-background;
    }
  }

  &.blue {
    color: $color-blue;

    &.background {
      background-color: $color-blue-background;
    }
  }

  *:hover > &.hover-blue,
  &.active.hover-blue {
    color: $color-blue;

    &.background {
      background-color: $color-blue-background;
    }
  }

  &.green {
    color: $color-green;

    &.background {
      background-color: $color-green-background;
    }
  }

  *:hover > &.hover-green,
  &.active.hover-green {
    color: $color-green;

    &.background {
      background-color: $color-green-background;
    }
  }

  &.yellow {
    color: $color-yellow;

    &.background {
      background-color: $color-yellow-background;
    }
  }

  *:hover > &.hover-yellow,
  &.active.hover-yellow {
    color: $color-yellow;

    &.background {
      background-color: $color-yellow-background;
    }
  }
}

@media (max-width: 768px) {
  .icon {
    &.background {
      width: 36px;
      height: 36px;
    }
  }
}
</style>