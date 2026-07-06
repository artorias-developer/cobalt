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
    type="button"
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
      background-color: color-mix(in srgb, var(--color-primary) 80%, transparent);
    }

    &.gray {
      background-color: color-mix(in srgb, var(--color-gray) 10%, transparent);
    }
  }

  &:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: -2px;
  }

  &:disabled {
    opacity: 0.5;
    pointer-events: none;
  }

  &.blue {
    background-color: var(--color-primary);
    color: var(--color-white);

    &:focus-visible {
      outline: 2px solid var(--color-red);
    }
  }

  &.gray {
    background-color: var(--color-gray-background);
    color: var(--color-description);
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