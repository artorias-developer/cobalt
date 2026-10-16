<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <button
    type="button"
    class="button"
    :class="buttonClasses"
    :name="name"
    :disabled="isLoading"
    :aria-busy="isLoading"
  >
    <Icon
      v-if="icon"
      :icon="icon"
      :base-color="baseColor"
      :hover-color="hoverColor"
      :is-active="false"
    />
    <span v-if="text">{{ text }}</span>
    <i
      v-if="showSpinner"
      class="spinner"
      aria-hidden="true"
      v-html="spinnerIcon"
    />
  </button>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from "vue"

import type { Color, ButtonAlign } from "@/types"

import Icon from "@/components/ui/Icon.vue"

import spinnerIcon from "@/assets/images/svg/spinner.svg?raw"

const SPINNER_DELAY_MS = 200

const props = defineProps<{
  icon?: string
  text?: string
  baseColor: Color
  hoverColor?: Color
  name?: string
  align?: ButtonAlign
  filled?: boolean
  isLoading?: boolean
}>()

const showSpinner = ref(false)

let spinnerTimer: ReturnType<typeof setTimeout> | null = null

/**
 * Returns whether the button is in "filled with text" mode.
 * In this mode the button itself gets a colored background instead of just the icon.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if filled and text are both provided.
 */
const isFilledWithText = computed((): boolean =>
  props.filled && !!props.text
)

/**
 * Returns the list of dynamic CSS classes for the button.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - string[]: Array of CSS class names based on current props and loading state.
 */
const buttonClasses = computed((): string[] => [
  props.baseColor,
  props.hoverColor ? `hover-${props.hoverColor}` : "",
  props.filled && !props.text ? "background" : "",
  isFilledWithText.value ? "background-text" : "",
  props.align ? `align-${props.align}` : "align-start",
  props.hoverColor && props.hoverColor === props.baseColor ? "same-color" : "",
  props.isLoading ? "loading" : "",
  showSpinner.value ? "content-hidden" : ""
])

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
  @include button-ghost-base;

  &:disabled {
    opacity: 0.5;
    pointer-events: none;
  }

  &.loading {
    pointer-events: none;
  }

  &.content-hidden > :not(.spinner) {
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