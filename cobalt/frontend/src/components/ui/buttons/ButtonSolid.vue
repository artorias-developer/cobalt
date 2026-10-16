<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <button
    :type="submit ? 'submit' : 'button'"
    :form="form"
    class="button"
    :class="[color, { loading: isLoading }]"
    :name="name"
    :disabled="isLoading"
    :aria-busy="isLoading"
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

import spinnerIcon from "@/assets/images/svg/spinner.svg?raw"

const SPINNER_DELAY_MS = 150

const props = defineProps<{
  text: string
  color: "blue" | "gray"
  name?: string
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
@use "@/assets/styles/mixins" as *;

.button {
  @include button-solid-base;

  &:disabled {
    opacity: 0.5;
    pointer-events: none;
  }

  &.loading {
    pointer-events: none;
  }

  span.hidden {
    visibility: hidden;
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
  .button .spinner {
    width: 18px;
    height: 18px;
    margin: -9px 0 0 -9px;
  }
}
</style>