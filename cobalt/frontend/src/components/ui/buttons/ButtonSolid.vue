<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <router-link
    v-if="type === 'router-link'"
    class="button"
    :class="[color, { loading:isLoading }]"
    :to="to!"
    :aria-label="name"
    :aria-busy="isLoading"
    :tabindex="isLoading ? -1 : 0"
  >
    <span :class="{ hidden: showSpinner }">{{ text }}</span>
    <i
      v-if="showSpinner"
      class="spinner"
      aria-hidden="true"
      v-html="spinnerIcon"
    />
  </router-link>
  <a
    v-else-if="type === 'a'"
    class="button"
    :class="[color, { loading:isLoading }]"
    :href="href"
    :target="target"
    :rel="target === '_blank' ? 'noopener noreferrer' : undefined"
    :aria-label="name"
    :aria-busy="isLoading"
    :tabindex="isLoading ? -1 : 0"
  >
    <span :class="{ hidden: showSpinner }">{{ text }}</span>
    <i
      v-if="showSpinner"
      class="spinner"
      aria-hidden="true"
      v-html="spinnerIcon"
    />
  </a>
  <button
    v-else
    :type="submit ? 'submit' : 'button'"
    :form="form"
    class="button"
    :class="[color, { loading:isLoading }]"
    :name="name"
    :disabled="isLoading"
    :aria-busy="isLoading"
    tabindex="0"
  >
    <span :class="{ hidden: showSpinner }">{{ text }}</span>
    <i
      v-if="showSpinner"
      class="spinner"
      aria-hidden="true"
      v-html="spinnerIcon"
    />
  </button>
</template>

<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from "vue"
import { type RouteLocationRaw } from "vue-router"

import type { ButtonTarget, ButtonType } from "@/types"

import spinnerIcon from "@/assets/images/svg/spinner.svg?raw"

const SPINNER_DELAY_MS = 1

const props = defineProps<{
  type: ButtonType
  text: string
  color: "blue" | "gray"
  name?: string
  href?: string
  to?: RouteLocationRaw
  target?: ButtonTarget
  submit?: boolean
  form?: string
  isLoading?: boolean
}>()

const showSpinner = ref(false)

let spinnerTimer: ReturnType<typeof setTimeout> | null = null

/**
 * Cancels the pending spinner timer if there is one.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function clearSpinnerTimer(): void {
  if (spinnerTimer !== null) {
    clearTimeout(spinnerTimer)
    spinnerTimer = null
  }
}

watch(
  () => props.isLoading,
  (loading) => {
    clearSpinnerTimer()

    if (!loading) {
      showSpinner.value = false

      return
    }

    spinnerTimer = setTimeout(() => {
      showSpinner.value = true
      spinnerTimer = null
    }, SPINNER_DELAY_MS)
  },
  { immediate: true }
)

onBeforeUnmount(clearSpinnerTimer)
</script>

<style scoped lang="scss">
.button {
  position: relative;
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
      background-color: color-mix(in srgb, var(--color-gray-background) 65%, transparent);
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

  &.loading {
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
    color: var(--color-gray);
  }

  span {
    font-size: $font-md;
    font-weight: 600;
    white-space: nowrap;

    &.hidden {
      visibility: hidden;
    }
  }

  .spinner {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    margin: -10px 0 0 -10px;
    display: flex;
    animation: button-spin 0.8s linear infinite;

    :deep(svg) {
      width: 100%;
      height: 100%;
    }
  }
}

@keyframes button-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .button {
    height: 36px;
    padding: 0 $space-lg;

    span {
      font-size: $font-sm;
    }

    .spinner {
      width: 18px;
      height: 18px;
      margin: -9px 0 0 -9px;
    }
  }
}
</style>