<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <router-link
    v-if="type === 'router-link'"
    class="button"
    :class="[color]"
    :to="to!"
    :aria-label="name"
    tabindex="0"
  >
    <span>{{ text }}</span>
  </router-link>
  <a
    v-else-if="type === 'a'"
    class="button"
    :class="[color]"
    :href="href"
    :target="target"
    :rel="target === '_blank' ? 'noopener noreferrer' : undefined"
    :aria-label="name"
    tabindex="0"
  >
    <span>{{ text }}</span>
  </a>
  <button
    v-else
    class="button"
    :class="[color]"
    :name="name"
    tabindex="0"
  >
    <span>{{ text }}</span>
  </button>
</template>

<script setup lang="ts">
import { type RouteLocationRaw } from "vue-router"

import type { ButtonTarget, ButtonType } from "@/types"

defineProps<{
  type: ButtonType
  text: string
  color: "blue" | "gray"
  name?: string
  href?: string
  to?: RouteLocationRaw
  target?: ButtonTarget
}>()
</script>

<style scoped lang="scss">
.button {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  outline: none;
  text-decoration: none;
  border-radius: 6px;
  padding: 0 $space-xl;
  transition: background-color 0.3s ease;
  box-sizing: border-box;

  &:hover {
    &.blue {
      background-color: rgba($color-primary, 0.8);
    }

    &.gray {
      background-color: rgba($color-gray-background, 0.1);
    }
  }

  &:focus-visible {
    outline: 2px solid $color-primary;
    outline-offset: -2px;
  }

  &.blue {
    background-color: $color-primary;
    color: $color-title;

    &:focus-visible {
      outline: 2px solid $color-red;
    }
  }

  &.gray {
    background-color: $color-gray-background;
    color: $color-text;
  }

  span {
    font-size: $font-md;
    font-weight: 600;
    white-space: nowrap;
  }
}

@media (max-width: 768px) {
  .button {
    height: 36px;
    padding: 0 $space-lg;

    span {
      font-size: $font-sm;
    }
  }
}
</style>